'use client';

import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { TrackballControls } from '@react-three/drei';
import { OBJLoader } from 'three-stdlib';
import { useMemo, Suspense, useRef, useEffect, useCallback } from 'react';
import * as THREE from 'three';
import type { TrackballControls as TrackballControlsType } from 'three-stdlib';

interface FractalViewerProps {
  objData: string | null;
  autoRotate?: boolean;
  onAutoRotateChange?: (autoRotate: boolean) => void;
}

// Parse OBJ data and return geometry info including bounding sphere radius
function parseObjData(objData: string): { geometry: THREE.BufferGeometry | null; radius: number } {
  const loader = new OBJLoader();
  const group = loader.parse(objData);

  let foundGeo: THREE.BufferGeometry | null = null;
  group.traverse((child) => {
    if (child instanceof THREE.Mesh && child.geometry) {
      foundGeo = child.geometry;
    }
  });

  if (!foundGeo) return { geometry: null, radius: 1 };

  const geo = foundGeo as THREE.BufferGeometry;

  // Compute bounding box to find the true visual center
  geo.computeBoundingBox();
  const box = geo.boundingBox!;

  // Calculate the center of the bounding box
  const center = new THREE.Vector3();
  box.getCenter(center);

  // Translate geometry so its bounding box center is at origin
  geo.translate(-center.x, -center.y, -center.z);

  // Compute bounding sphere for camera distance calculation
  geo.computeBoundingSphere();
  const radius = geo.boundingSphere?.radius || 1;

  return { geometry: geo, radius };
}

function FractalModel({ objData, onRadiusChange }: { objData: string; onRadiusChange?: (radius: number) => void }) {
  const { geometry, radius } = useMemo(() => parseObjData(objData), [objData]);

  // Notify parent of radius change
  useEffect(() => {
    if (onRadiusChange && radius) {
      onRadiusChange(radius);
    }
  }, [radius, onRadiusChange]);

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

// Calculate camera distance based on model bounding sphere radius
function calculateCameraDistance(radius: number): number {
  // Position camera so model fills ~60% of viewport vertically
  // For 45° FOV, distance = radius / tan(FOV/2) * factor
  // factor > 1 gives more margin around the model
  return radius * 2.8;
}

// Default initial distance before model loads
const DEFAULT_CAMERA_DISTANCE = 12;

// Scene content with orbit animation
function SceneContent({
  objData,
  autoRotate,
  onAutoRotateChange,
}: {
  objData: string | null;
  autoRotate: boolean;
  onAutoRotateChange?: (autoRotate: boolean) => void;
}) {
  const { camera } = useThree();
  const controlsRef = useRef<TrackballControlsType>(null);
  const timeRef = useRef(0);
  const wasAutoRotating = useRef(false);

  // Animation parameters
  const spinSpeed = 0.5; // Speed of the spin (radians per second)

  // Store the base spherical coordinates (captured from current camera position)
  // For Z-up: phi is angle from Z axis, theta is rotation in XY plane
  // phi = PI/2 - 0.3 (slightly above horizontal), theta = PI/4 (45° in XY plane)
  const baseSpherical = useRef(new THREE.Spherical(DEFAULT_CAMERA_DISTANCE, Math.PI / 2 - 0.3, Math.PI / 4));

  // Track applied camera distance (only updates when model loads)
  const appliedCameraDistance = useRef(DEFAULT_CAMERA_DISTANCE);

  // Callback when model reports its radius
  const handleRadiusChange = useCallback((radius: number) => {
    const newDistance = calculateCameraDistance(radius);
    appliedCameraDistance.current = newDistance;

    // Update camera position to new distance while maintaining angle
    const spherical = new THREE.Spherical();
    spherical.setFromVector3(camera.position);
    spherical.radius = newDistance;
    const newPos = new THREE.Vector3().setFromSpherical(spherical);
    camera.position.copy(newPos);
    baseSpherical.current.radius = newDistance;

    // Update optical center offset
    const newOffset = -newDistance * 0.08;
    camera.lookAt(0, 0, newOffset);
    if (controlsRef.current) {
      controlsRef.current.target.set(0, 0, newOffset);
      controlsRef.current.update();
    }
  }, [camera]);

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

    timeRef.current += delta * spinSpeed;

    // Rotate around the Z axis (pyramid's vertical axis from base to tip)
    // Keep the same distance and Z height, rotate in the XY plane
    const basePos = new THREE.Vector3().setFromSpherical(baseSpherical.current);
    const xyDistance = Math.sqrt(basePos.x * basePos.x + basePos.y * basePos.y);
    const baseAngle = Math.atan2(basePos.y, basePos.x);

    const newAngle = baseAngle + timeRef.current;
    const newX = xyDistance * Math.cos(newAngle);
    const newY = xyDistance * Math.sin(newAngle);

    camera.position.set(newX, newY, basePos.z);
    camera.up.set(0, 0, 1);
    // Look at the optical center offset point (use applied distance, not pending)
    camera.lookAt(0, 0, -appliedCameraDistance.current * 0.08);

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
        {objData && <FractalModel objData={objData} onRadiusChange={handleRadiusChange} />}
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

export function FractalViewer({ objData, autoRotate = true, onAutoRotateChange }: FractalViewerProps) {
  // Camera position for side view with pyramid base pointing down
  // The model has Z as vertical axis, so we position camera in XY plane with slight elevation
  // 45-degree angle in XY plane, slightly above Z=0 to see the 3D shape
  const angle = Math.PI / 4; // 45 degrees in XY plane
  const elevation = 0.3; // Slight elevation to see 3D nature
  const initialX = DEFAULT_CAMERA_DISTANCE * Math.cos(angle) * Math.cos(elevation);
  const initialY = DEFAULT_CAMERA_DISTANCE * Math.sin(angle) * Math.cos(elevation);
  const initialZ = DEFAULT_CAMERA_DISTANCE * Math.sin(elevation);

  return (
    <div className="w-full h-dvh bg-gray-950">
      <Canvas camera={{ position: [initialX, initialY, initialZ], fov: 45, up: [0, 0, 1] }}>
        <SceneContent objData={objData} autoRotate={autoRotate} onAutoRotateChange={onAutoRotateChange} />
      </Canvas>
    </div>
  );
}
