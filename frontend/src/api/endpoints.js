import client from "./client";

export const authApi = {
  login: (data) => client.post("/auth/login", data),
  me: () => client.get("/auth/me"),
};

export const matriculaApi = {
  listar: () => client.get("/matricula"),
  solicitar: (data) => client.post("/matricula", data),
  validar: (id, data) => client.patch(`/matricula/${id}/validar`, data),
  estadisticas: () => client.get("/matricula/estadisticas"),
  descargarFicha: (id) => client.get(`/matricula/${id}/ficha`, { responseType: "blob" }),
};

export const cursoApi = {
  listar: (params) => client.get("/cursos", { params }),
  docentes: () => client.get("/cursos/docentes"),
  cargarSilabo: (id, data) => client.post(`/cursos/${id}/silabo`, data),
  asignar: (id, data) => client.patch(`/cursos/${id}/asignar`, data),
  cargaDocente: () => client.get("/cursos/carga-docente"),
};

export const notaApi = {
  listar: (params) => client.get("/notas", { params }),
  registrar: (data) => client.post("/notas", data),
  validar: (id) => client.patch(`/notas/${id}/validar`),
  indicadores: () => client.get("/notas/indicadores"),
  estudiantesCurso: (cursoId) => client.get(`/notas/estudiantes-curso/${cursoId}`),
  consolidado: () => client.get("/notas/consolidado"),
  consolidar: (curso_id, periodo) => client.patch("/notas/consolidar", { curso_id, periodo }),
};

export const recordApi = {
  estudiante: (id) => client.get(`/record/${id}`),
  consolidado: () => client.get("/record/reportes/consolidado"),
};

export const certificadoApi = {
  listar: () => client.get("/certificados"),
  solicitar: (data) => client.post("/certificados", data),
  autorizar: (id) => client.patch(`/certificados/${id}/autorizar`),
  emitir: (id, metodo = "ambos") => client.patch(`/certificados/${id}/emitir`, { metodo }),
  descargarPdf: (id) => client.get(`/certificados/${id}/pdf`, { responseType: "blob" }),
  // Verificación pública: no requiere token (se usa desde /verificar/:codigo)
  verificar: (codigo) => client.get(`/certificados/verificar/${codigo}`),
};

export const seguridadApi = {
  usuarios: (params) => client.get("/usuarios", { params }),
  crearUsuario: (data) => client.post("/usuarios", data),
  actualizarUsuario: (id, data) => client.patch(`/usuarios/${id}`, data),
  auditoria: () => client.get("/seguridad/auditoria"),
};
