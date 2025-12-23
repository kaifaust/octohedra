'use client';

import { Canvas } from '@react-three/fiber';
import { OrbitControls, Center, Environment } from '@react-three/drei';
import { OBJLoader } from 'three-stdlib';
import { useMemo, Suspense } from 'react';
import * as THREE from 'three';

interface FractalViewerProps {
  objData: string | null;
}

function FractalModel({ objData }: { objData: string }) {
  const geometry = useMemo(() => {
    const loader = new OBJLoader();
    const group = loader.parse(objData);

    let geometry: THREE.BufferGeometry | null = null;
    group.traverse((child) => {
      if (child instanceof THREE.Mesh && child.geometry) {
        geometry = child.geometry;
      }
    });

    return geometry;
  }, [objData]);

  if (!geometry) return null;

  return (
    <Center>
      <mesh geometry={geometry}>
        <meshStandardMaterial
          color="#4080ff"
          metalness={0.3}
          roughness={0.4}
          side={THREE.DoubleSide}
        />
      </mesh>
    </Center>
  );
}

export function FractalViewer({ objData }: FractalViewerProps) {
  return (
    <div className="w-full h-[600px] bg-gray-900 rounded-lg overflow-hidden">
      <Canvas camera={{ position: [50, 50, 50], fov: 50 }}>
        <ambientLight intensity={0.5} />
        <directionalLight position={[10, 10, 5]} intensity={1} />
        <Suspense fallback={null}>
          {objData && <FractalModel objData={objData} />}
          <Environment preset="studio" />
        </Suspense>
        <OrbitControls enablePan={true} enableZoom={true} enableRotate={true} />
      </Canvas>
    </div>
  );
}
