import { useEffect } from "react";

export default function Toast({ mensaje, onClose }) {
  useEffect(() => {
    if (!mensaje) return;
    const t = setTimeout(onClose, 2800);
    return () => clearTimeout(t);
  }, [mensaje, onClose]);
  if (!mensaje) return null;
  return <div className="toast">{mensaje}</div>;
}
