import { Routes, Route, Navigate } from "react-router-dom";
import ProtectedRoute from "./routes/ProtectedRoute";
import DashboardLayout from "./layouts/DashboardLayout";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Matricula from "./pages/Matricula";
import Cursos from "./pages/Cursos";
import Notas from "./pages/Notas";
import Record from "./pages/Record";
import Certificados from "./pages/Certificados";
import Usuarios from "./pages/Usuarios";
import Auditoria from "./pages/Auditoria";
import VerificarCertificado from "./pages/VerificarCertificado";

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      {/* Pública: destino del QR de un certificado, no requiere sesión */}
      <Route path="/verificar/:codigo" element={<VerificarCertificado />} />

      <Route element={<ProtectedRoute><DashboardLayout /></ProtectedRoute>}>
        <Route path="/" element={<Dashboard />} />

        <Route path="/matricula" element={
          <ProtectedRoute roles={["estudiante", "admin", "direccion"]}><Matricula /></ProtectedRoute>} />

        <Route path="/cursos" element={
          <ProtectedRoute roles={["docente", "admin", "direccion"]}><Cursos /></ProtectedRoute>} />

        <Route path="/notas" element={
          <ProtectedRoute roles={["estudiante", "docente", "admin"]}><Notas /></ProtectedRoute>} />

        <Route path="/record" element={
          <ProtectedRoute roles={["estudiante", "admin", "direccion"]}><Record /></ProtectedRoute>} />

        <Route path="/certificados" element={
          <ProtectedRoute roles={["estudiante", "admin", "direccion"]}><Certificados /></ProtectedRoute>} />

        <Route path="/usuarios" element={
          <ProtectedRoute roles={["admin"]}><Usuarios /></ProtectedRoute>} />

        <Route path="/auditoria" element={
          <ProtectedRoute roles={["direccion", "admin"]}><Auditoria /></ProtectedRoute>} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
