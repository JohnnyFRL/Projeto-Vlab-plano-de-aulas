import { useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { usePlans } from "../hooks/usePlans";
import { api } from "../services/api";
import Filters from "../components/Filters";
import PlanCard from "../components/PlanCard";
import Pagination from "../components/Pagination";
import Toast from "../components/Toast";
import styles from "./ListPage.module.css";

const DEFAULT_FILTERS = {
  search: "",
  discipline: "",
  tag: "",
  planned_date: "",
  sort: "created_at",
  page: 1,
  limit: 9,
};

export default function ListPage() {
  const navigate = useNavigate();
  const [filters, setFilters] = useState(DEFAULT_FILTERS);
  const [toast, setToast] = useState(null);

  const { data, meta, loading, error, refetch } = usePlans(filters);

  const showToast = useCallback((message, type = "success") => {
    setToast({ message, type });
  }, []);

  async function handleDelete(id) {
    try {
      await api.remove(id);
      showToast("Plano removido com sucesso.");
      refetch();
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  function handlePageChange(page) {
    setFilters((f) => ({ ...f, page }));
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  return (
    <div className={styles.page}>
      <div className={styles.header}>
        <div>
          <h1 className={styles.title}>Planos de Aula</h1>
          <p className={styles.subtitle}>
            {meta.total > 0 ? `${meta.total} plano${meta.total !== 1 ? "s" : ""} cadastrado${meta.total !== 1 ? "s" : ""}` : "Nenhum plano ainda"}
          </p>
        </div>
        <button className={styles.newBtn} onClick={() => navigate("/planos/novo")}>
          + Novo Plano
        </button>
      </div>

      <Filters filters={filters} onChange={setFilters} />

      {loading && (
        <div className={styles.state}>
          <div className={styles.spinner} />
          <span>Carregando...</span>
        </div>
      )}

      {error && !loading && (
        <div className={styles.stateError}>
          <p>Erro ao carregar planos.</p>
          <p className={styles.stateDetail}>{error}</p>
          <button className={styles.retryBtn} onClick={refetch}>Tentar novamente</button>
        </div>
      )}

      {!loading && !error && data.length === 0 && (
        <div className={styles.state}>
          <p className={styles.emptyTitle}>Nenhum plano encontrado</p>
          <p className={styles.emptySubtitle}>
            {filters.search || filters.discipline || filters.tag
              ? "Tente ajustar os filtros."
              : "Crie seu primeiro plano de aula."}
          </p>
          {!filters.search && !filters.discipline && !filters.tag && (
            <button className={styles.createBtn} onClick={() => navigate("/planos/novo")}>
              Criar plano
            </button>
          )}
        </div>
      )}

      {!loading && !error && data.length > 0 && (
        <>
          <div className={styles.grid}>
            {data.map((plan) => (
              <PlanCard key={plan.id} plan={plan} onDelete={handleDelete} />
            ))}
          </div>

          <Pagination
            page={meta.page}
            pages={meta.pages}
            total={meta.total}
            onChange={handlePageChange}
          />
        </>
      )}

      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}
    </div>
  );
}
