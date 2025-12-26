'use client';

import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { TrackballControls } from '@react-three/drei';
import { OBJLoader } from 'three-stdlib';
import { useMemo, Suspense, useRef, useEffect, useCallback, useImperativeHandle, forwardRef } from 'react';
import * as THREE from 'three';
import type { TrackballControls as TrackballControlsType } from 'three-stdlib';

export interface FractalViewerHandle {
  captureScreenshot: () => Promise<Blob | null>;
}

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

  // Recompute bounding box after centering (for color calculation)
  geo.computeBoundingBox();
  const centeredBox = geo.boundingBox!;

  // Add vertex colors based on Z position (rainbow from bottom to top)
  const positions = geo.attributes.position;
  const colors = new Float32Array(positions.count * 3);
  const color = new THREE.Color();

  const minZ = centeredBox.min.z;
  const maxZ = centeredBox.max.z;
  const zRange = maxZ - minZ || 1;

  for (let i = 0; i < positions.count; i++) {
    const z = positions.getZ(i);
    // Normalize Z to 0-1 range (bottom to top)
    const t = (z - minZ) / zRange;

    // Rainbow: red (0) -> orange -> yellow -> green -> cyan -> blue -> violet (0.85)
    // Using HSL with hue from 0 (red) to ~0.85 (violet) gives a nice rainbow
    const hue = t * 0.85;
    color.setHSL(hue, 0.9, 0.55);

    colors[i * 3] = color.r;
    colors[i * 3 + 1] = color.g;
    colors[i * 3 + 2] = color.b;
  }

  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));

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
        vertexColors={true}
        emissive="#ffffff"
        emissiveIntensity={0.08}
        metalness={0.1}
        roughness={0.5}
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
  const mainLightRef = useRef<THREE.DirectionalLight>(null);
  const fillLightRef = useRef<THREE.DirectionalLight>(null);

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
    }

    if (autoRotate) {
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
    }

    // Update lights to follow camera (relative to camera orientation)
    if (mainLightRef.current && fillLightRef.current) {
      // Get camera's right and up vectors
      const right = new THREE.Vector3();
      const up = new THREE.Vector3();
      camera.getWorldDirection(new THREE.Vector3());
      right.setFromMatrixColumn(camera.matrixWorld, 0);
      up.setFromMatrixColumn(camera.matrixWorld, 1);

      // Main light: upper-right relative to camera
      const mainLightPos = camera.position.clone()
        .add(right.clone().multiplyScalar(10))
        .add(up.clone().multiplyScalar(8));
      mainLightRef.current.position.copy(mainLightPos);

      // Fill light: upper-left relative to camera
      const fillLightPos = camera.position.clone()
        .add(right.clone().multiplyScalar(-10))
        .add(up.clone().multiplyScalar(8));
      fillLightRef.current.position.copy(fillLightPos);
    }
  });

  return (
    <>
      <ambientLight intensity={0.1} />
      <directionalLight
        ref={mainLightRef}
        position={[10, 8, 12]}
        intensity={1}
        color="#ffffff"
      />
      <directionalLight
        ref={fillLightRef}
        position={[-10, -8, 12]}
        intensity={0.6}
        color="#ffffff"
      />
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

export const FractalViewer = forwardRef<FractalViewerHandle, FractalViewerProps>(
  function FractalViewer({ objData, autoRotate = true, onAutoRotateChange }, ref) {
    const canvasRef = useRef<HTMLCanvasElement>(null);

    // Camera position for side view with pyramid base pointing down
    // The model has Z as vertical axis, so we position camera in XY plane with slight elevation
    // 45-degree angle in XY plane, slightly above Z=0 to see the 3D shape
    const angle = Math.PI / 4; // 45 degrees in XY plane
    const elevation = 0.3; // Slight elevation to see 3D nature
    const initialX = DEFAULT_CAMERA_DISTANCE * Math.cos(angle) * Math.cos(elevation);
    const initialY = DEFAULT_CAMERA_DISTANCE * Math.sin(angle) * Math.cos(elevation);
    const initialZ = DEFAULT_CAMERA_DISTANCE * Math.sin(elevation);

    // Expose screenshot capture to parent
    useImperativeHandle(ref, () => ({
      captureScreenshot: async () => {
        const canvas = canvasRef.current;
        if (!canvas) return null;

        return new Promise<Blob | null>((resolve) => {
          canvas.toBlob((blob) => {
            resolve(blob);
          }, 'image/png');
        });
      },
    }), []);

    return (
      <div className="w-full h-dvh bg-gray-950">
        <Canvas
          ref={canvasRef}
          camera={{ position: [initialX, initialY, initialZ], fov: 45, up: [0, 0, 1] }}
          gl={{ preserveDrawingBuffer: true }}
        >
          <SceneContent objData={objData} autoRotate={autoRotate} onAutoRotateChange={onAutoRotateChange} />
        </Canvas>
      </div>
    );
  }
);
