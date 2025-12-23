'use client';

import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { TrackballControls, Environment } from '@react-three/drei';
import { OBJLoader } from 'three-stdlib';
import { useMemo, Suspense, useRef } from 'react';
import * as THREE from 'three';
import type { TrackballControls as TrackballControlsType } from 'three-stdlib';

interface FractalViewerProps {
  objData: string | null;
  depth?: number;
  autoRotate?: boolean;
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
        color="#4080ff"
        metalness={0.3}
        roughness={0.4}
        side={THREE.DoubleSide}
      />
    </mesh>
  );
}

// Scene content with orbit animation
function SceneContent({
  objData,
  autoRotate
}: {
  objData: string | null;
  autoRotate: boolean;
}) {
  const { camera } = useThree();
  const controlsRef = useRef<TrackballControlsType>(null);
  const timeRef = useRef(0);
  const wasAutoRotating = useRef(false);

  // Animation parameters
  const orbitSpeed = 2.4; // Speed of the orbit (radians per second)

  // Store the base spherical coordinates (captured from current camera position)
  const baseSpherical = useRef(new THREE.Spherical(70, Math.PI / 2.2, 0));

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

    // Apply to camera position using spherical coordinates
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

  return (
    <>
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} intensity={1} />
      <Suspense fallback={null}>
        {objData && <FractalModel objData={objData} />}
        <Environment preset="studio" />
      </Suspense>
      <TrackballControls
        ref={controlsRef}
        noPan={false}
        noZoom={false}
        noRotate={false}
        rotateSpeed={2}
        zoomSpeed={1.2}
        panSpeed={0.8}
      />
    </>
  );
}

export function FractalViewer({ objData, depth = 2, autoRotate = true }: FractalViewerProps) {
  return (
    <div className="w-full h-dvh bg-gray-950">
      <Canvas camera={{ position: [0, 5, 70], fov: 45 }}>
        <SceneContent objData={objData} autoRotate={autoRotate} />
      </Canvas>
    </div>
  );
}
