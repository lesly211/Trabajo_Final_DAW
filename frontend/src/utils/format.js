export const rolLabel = {
  estudiante: "Estudiante",
  docente: "Docente",
  admin: "Administrador",
  direccion: "Dirección",
};

export const estadoBadge = (estado) => {
  const map = {
    pendiente: "badge-warn",
    solicitado: "badge-warn",
    validada: "badge-ok",
    emitido: "badge-ok",
    rechazada: "badge-danger",
    Aprobado: "badge-ok",
    Desaprobado: "badge-danger",
  };
  return map[estado] || "badge-neutral";
};
