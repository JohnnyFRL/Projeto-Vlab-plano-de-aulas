import { Routes, Route, Navigate } from "react-router-dom";
import Layout from "./components/Layout";
import ListPage from "./pages/ListPage";
import FormPage from "./pages/FormPage";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Navigate to="/planos" replace />} />
        <Route path="planos" element={<ListPage />} />
        <Route path="planos/novo" element={<FormPage />} />
        <Route path="planos/:id/editar" element={<FormPage />} />
      </Route>
    </Routes>
  );
}
