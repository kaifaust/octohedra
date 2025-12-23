'use client';

import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { TrackballControls } from '@react-three/drei';
import { OBJLoader } from 'three-stdlib';
import { useMemo, Suspense, useRef } from 'react';
import * as THREE from 'three';
import type { TrackballControls as TrackballControlsType } from 'three-stdlib';

interface FractalViewerProps {
  objData: string | null;
  totalDepth?: number; // Sum of all layer depths for zoom calculation
  autoRotate?: boolean;
  onAutoRotateChange?: (autoRotate: boolean) => void;
}

function FractalModel({ objData }: { objData: string }) {
  const { geometry, offset } = useMemo(() => {
    const loader = new OBJLoader();
    const group = loader.parse(objData);

    let geo: THREE.BufferGeometry | null = null;
    group.traverse((child) => {
      if (child instanceof THREE.Mesh && child.geometry) {
        geo = child.geometry;
      }
    });

    if (!geo) return { geometry: null, offset: new THREE.Vector3() };

    // Compute bounding box to find the true visual center
    geo.computeBoundingBox();
    const box = geo.boundingBox!;

    // Calculate the center of the bounding box
    const center = new THREE.Vector3();
    box.getCenter(center);

    // Translate geometry so its bounding box center is at origin
    geo.translate(-center.x, -center.y, -center.z);

    return { geometry: geo, offset: center };
  }, [objData]);

  if (!geometry) return null;

  return (
    <mesh geometry={geometry}>
      <meshStandardMaterial
        color="#5ce1f5"
        metalness={0.25}
        roughness={0.3}
        side={THREE.DoubleSide}
      />
    </mesh>
  );
}

// Calculate camera distance based on total depth
function calculateCameraDistance(totalDepth: number): number {
  // Base distance for depth 3 (single flake)
  const baseDistance = 12;
  // Linear scale: add distance for each depth unit above 3
  const additionalDistance = (totalDepth - 3) * 3;
  return baseDistance + additionalDistance;
}

// Scene content with orbit animation
function SceneContent({
  objData,
  autoRotate,
  onAutoRotateChange,
  totalDepth
}: {
  objData: string | null;
  autoRotate: boolean;
  onAutoRotateChange?: (autoRotate: boolean) => void;
  totalDepth: number;
}) {
  const { camera } = useThree();
  const controlsRef = useRef<TrackballControlsType>(null);
  const timeRef = useRef(0);
  const wasAutoRotating = useRef(false);

  // Animation parameters
  const orbitSpeed = 2.4; // Speed of the orbit (radians per second)

  // Calculate camera distance based on total depth
  const cameraDistance = calculateCameraDistance(totalDepth);

  // Store the base spherical coordinates (captured from current camera position)
  const baseSpherical = useRef(new THREE.Spherical(cameraDistance, Math.PI / 2, 0));

  // Track previous objData to detect when new model renders
  const prevObjData = useRef(objData);
  const pendingDistance = useRef(cameraDistance);

  // Always update pending distance when totalDepth changes
  pendingDistance.current = cameraDistance;

  // Only update camera when new model data arrives
  if (prevObjData.current !== objData && objData !== null) {
    // Update camera position to new distance while maintaining angle
    const spherical = new THREE.Spherical();
    spherical.setFromVector3(camera.position);
    spherical.radius = pendingDistance.current;
    const newPos = new THREE.Vector3().setFromSpherical(spherical);
    camera.position.copy(newPos);
    baseSpherical.current.radius = pendingDistance.current;
    prevObjData.current = objData;
  }

  useFrame((_, delta) => {
    if (!controlsRef.current) return;

    // When auto-rotate is enabled, capture current camera position as the base
    if (autoRotate && !wasAutoRotating.current) {
      const spherical = new THREE.Spherical();
      spherical.setFromVector3(camera.position);
      baseSpherical.current.copy(spherical);
      wasAutoRotating.current = true;
    } else if (!autoRotate) {
      wasAutoRotating.current = false;
      return;
    }

    timeRef.current += delta * orbitSpeed;

    // Calculate orbital offset in spherical coordinates
    const thetaOffset = Math.sin(timeRef.current) * 0.4; // Azimuthal wobble (left/right)
    const phiOffset = Math.cos(timeRef.current) * 0.25; // Polar wobble (up/down)

    // Apply to camera position using spherical coordinates (use current radius, not pending)
    const spherical = new THREE.Spherical(
      baseSpherical.current.radius,
      baseSpherical.current.phi + phiOffset,
      baseSpherical.current.theta + thetaOffset
    );

    const newPos = new THREE.Vector3().setFromSpherical(spherical);
    camera.position.copy(newPos);
    camera.lookAt(0, 0, 0);

    // Update controls to match
    controlsRef.current.update();
  });

  // Three-point lighting rig that follows the camera
  const keyLightRef = useRef<THREE.DirectionalLight>(null);
  const fillLightRef = useRef<THREE.DirectionalLight>(null);
  const backLightRef = useRef<THREE.DirectionalLight>(null);

  // Update lights to follow camera orientation each frame
  useFrame(() => {
    // Get camera's right and up vectors in world space
    const right = new THREE.Vector3(1, 0, 0).applyQuaternion(camera.quaternion);
    const up = new THREE.Vector3(0, 1, 0).applyQuaternion(camera.quaternion);
    const forward = new THREE.Vector3(0, 0, -1).applyQuaternion(camera.quaternion);

    // Key light: main light, slightly right and above camera
    if (keyLightRef.current) {
      const keyPos = camera.position.clone()
        .add(right.clone().multiplyScalar(8))
        .add(up.clone().multiplyScalar(6));
      keyLightRef.current.position.copy(keyPos);
      keyLightRef.current.target.position.set(0, 0, 0);
      keyLightRef.current.target.updateMatrixWorld();
    }

    // Fill light: softer light on opposite side, slightly lower
    if (fillLightRef.current) {
      const fillPos = camera.position.clone()
        .add(right.clone().multiplyScalar(-6))
        .add(up.clone().multiplyScalar(2));
      fillLightRef.current.position.copy(fillPos);
      fillLightRef.current.target.position.set(0, 0, 0);
      fillLightRef.current.target.updateMatrixWorld();
    }

    // Back/rim light: behind and above the subject relative to camera
    if (backLightRef.current) {
      const backPos = new THREE.Vector3(0, 0, 0)
        .add(forward.clone().multiplyScalar(15))
        .add(up.clone().multiplyScalar(10));
      backLightRef.current.position.copy(backPos);
      backLightRef.current.target.position.set(0, 0, 0);
      backLightRef.current.target.updateMatrixWorld();
    }
  });

  return (
    <>
      <ambientLight intensity={0.15} />
      {/* Key light - main illumination, right and above */}
      <directionalLight ref={keyLightRef} intensity={1.2} color="#ffffff" />
      {/* Fill light - softer, opposite side */}
      <directionalLight ref={fillLightRef} intensity={0.4} color="#e0e8ff" />
      {/* Back/rim light - creates edge definition */}
      <directionalLight ref={backLightRef} intensity={0.2} color="#fff5e0" />
      <Suspense fallback={null}>
        {objData && <FractalModel objData={objData} />}
      </Suspense>
      <TrackballControls
        ref={controlsRef}
        noPan={false}
        noZoom={false}
        noRotate={false}
        rotateSpeed={2}
        zoomSpeed={1.2}
        panSpeed={0.8}
        onStart={() => {
          if (autoRotate && onAutoRotateChange) {
            onAutoRotateChange(false);
          }
        }}
      />
    </>
  );
}

export function FractalViewer({ objData, totalDepth = 3, autoRotate = true, onAutoRotateChange }: FractalViewerProps) {
  const initialDistance = calculateCameraDistance(totalDepth);

  return (
    <div className="w-full h-dvh bg-gray-950">
      <Canvas camera={{ position: [0, 0, initialDistance], fov: 45 }}>
        <SceneContent objData={objData} autoRotate={autoRotate} onAutoRotateChange={onAutoRotateChange} totalDepth={totalDepth} />
      </Canvas>
    </div>
  );
}
