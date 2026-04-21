import { Canvas } from '@react-three/fiber'
import { OrbitControls, Line, Stars } from '@react-three/drei'
import { useMemo, useState } from 'react'

function Node({ point, active, onClick }) {
  return (
    <mesh position={[point.x * 6, point.y * 6, point.z * 6]} onClick={() => onClick(point)}>
      <sphereGeometry args={[active ? 0.2 : 0.12, 16, 16]} />
      <meshStandardMaterial color={active ? '#5cf2ff' : '#7f5cff'} emissive={active ? '#5cf2ff' : '#1b1238'} />
    </mesh>
  )
}

export default function ThreeGraph({ points, highlightedIds }) {
  const [selected, setSelected] = useState(null)
  const highlighted = useMemo(() => new Set(highlightedIds), [highlightedIds])

  const lines = useMemo(() => {
    if (points.length < 2) return []
    const out = []
    for (let i = 1; i < points.length; i++) {
      out.push([points[i - 1], points[i]])
    }
    return out
  }, [points])

  return (
    <div className="panel graph-wrap">
      <Canvas camera={{ position: [0, 0, 12], fov: 50 }}>
        <color attach="background" args={['#070913']} />
        <ambientLight intensity={0.7} />
        <pointLight position={[10, 10, 10]} intensity={1.2} />
        <Stars radius={100} depth={50} count={2000} factor={4} saturation={0} fade speed={1} />

        {lines.map((pair, i) => (
          <Line
            key={i}
            points={[
              [pair[0].x * 6, pair[0].y * 6, pair[0].z * 6],
              [pair[1].x * 6, pair[1].y * 6, pair[1].z * 6],
            ]}
            color="#2b3a66"
            lineWidth={0.8}
          />
        ))}

        {points.map((p) => (
          <Node key={p.chunk_id} point={p} active={highlighted.has(p.chunk_id)} onClick={setSelected} />
        ))}

        <OrbitControls enablePan enableZoom autoRotate autoRotateSpeed={0.4} />
      </Canvas>
      {selected && (
        <div className="node-details">
          <h4>{selected.chunk_id}</h4>
          <p>{selected.text}</p>
        </div>
      )}
    </div>
  )
}
