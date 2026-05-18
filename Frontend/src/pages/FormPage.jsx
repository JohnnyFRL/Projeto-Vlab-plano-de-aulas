import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { api } from "../services/api";
import Toast from "../components/Toast";
import styles from "./FormPage.module.css";

const EMPTY = {
  title: "",
  discipline: "",
  objective: "",
  summary: "",
  planned_date: "",
  contents: "",
  support_resources: "",
  tags: "",
};

export default function FormPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const isEditing = Boolean(id);

  const [form, setForm] = useState(EMPTY);
  const [errors, setErrors] = useState({});
  const [saving, setSaving] = useState(false);
  const [loadingAI, setLoadingAI] = useState(false);
  const [fetching, setFetching] = useState(isEditing);
  const [toast, setToast] = useState(null);

  useEffect(() => {
    if (!isEditing) return;
    api.get(id)
      .then((plan) => {
        setForm({
          title: plan.title || "",
          discipline: plan.discipline || "",
          objective: plan.objective || "",
          summary: plan.summary || "",
          planned_date: plan.planned_date || "",
          contents: plan.contents || "",
          support_resources: plan.support_resources || "",
          tags: plan.tags || "",
        });
      })
      .catch(() => setToast({ message: "Erro ao carregar plano.", type: "error" }))
      .finally(() => setFetching(false));
  }, [id, isEditing]);

  function handle(e) {
    const { name, value } = e.target;
    setForm((f) => ({ ...f, [name]: value }));
    if (errors[name]) setErrors((e) => ({ ...e, [name]: null }));
  }

  function validate() {
    const e = {};
    if (!form.title.trim()) e.title = "Título é obrigatório.";
    if (!form.discipline.trim()) e.discipline = "Disciplina é obrigatória.";
    if (!form.objective.trim()) e.objective = "Objetivo é obrigatório.";
    if (!form.summary.trim()) e.summary = "Resumo é obrigatório.";
    if (!form.planned_date) e.planned_date = "Data prevista é obrigatória.";
    return e;
  }

  async function handleSubmit(e) {
    e.preventDefault();
    const errs = validate();
    if (Object.keys(errs).length > 0) { setErrors(errs); return; }

    setSaving(true);
    try {
      if (isEditing) {
        await api.update(id, form);
        setToast({ message: "Plano atualizado com sucesso." });
      } else {
        await api.create(form);
        setToast({ message: "Plano criado com sucesso." });
        setTimeout(() => navigate("/planos"), 1200);
      }
    } catch (err) {
      setToast({ message: err.message, type: "error" });
    } finally {
      setSaving(false);
    }
  }

  async function handleAI() {
    if (!form.title.trim() || !form.discipline.trim() || !form.summary.trim()) {
      setToast({
        message: "Preencha Título, Disciplina e Resumo antes de gerar sugestões.",
        type: "warning",
      });
      return;
    }

    setLoadingAI(true);
    try {
      const result = await api.aiSuggestions({
        title: form.title,
        discipline: form.discipline,
        summary: form.summary,
      });

      if (result.error) {
        setToast({ message: result.error, type: "error" });
        return;
      }

      setForm((f) => ({
        ...f,
        contents: result.contents?.join("\n") || f.contents,
        support_resources: result.support_resources?.join("\n") || f.support_resources,
        tags: result.recommended_tags?.join(",") || f.tags,
      }));

      setToast({ message: "Sugestões geradas com sucesso!" });
    } catch (err) {
      setToast({ message: "Não foi possível gerar sugestões agora.", type: "error" });
    } finally {
      setLoadingAI(false);
    }
  }

  if (fetching) {
    return (
      <div className={styles.loading}>
        <div className={styles.spinner} />
        <span>Carregando plano...</span>
      </div>
    );
  }

  return (
    <div className={styles.page}>
      <div className={styles.header}>
        <button className={styles.backBtn} onClick={() => navigate("/planos")}>
          ← Voltar
        </button>
        <h1 className={styles.title}>
          {isEditing ? "Editar Plano" : "Novo Plano de Aula"}
        </h1>
      </div>

      <form className={styles.form} onSubmit={handleSubmit} noValidate>

        {/* ── Informações básicas ── */}
        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>Informações básicas</h2>

          <div className={styles.row2}>
            <Field label="Título da Aula *" error={errors.title}>
              <input name="title" value={form.title} onChange={handle} placeholder="Ex: Introdução ao OSPF" />
            </Field>
            <Field label="Disciplina *" error={errors.discipline}>
              <input name="discipline" value={form.discipline} onChange={handle} placeholder="Ex: Redes de Computadores" />
            </Field>
          </div>

          <div className={styles.row2}>
            <Field label="Data Prevista *" error={errors.planned_date}>
              <input type="date" name="planned_date" value={form.planned_date} onChange={handle} />
            </Field>
            <Field label="Tags">
              <input name="tags" value={form.tags} onChange={handle} placeholder="redes,ospf,routing (separadas por vírgula)" />
            </Field>
          </div>

          <Field label="Objetivo *" error={errors.objective}>
            <textarea name="objective" value={form.objective} onChange={handle} rows={2} placeholder="O que o aluno vai aprender?" />
          </Field>

          <Field label="Resumo / Ementa *" error={errors.summary}>
            <textarea name="summary" value={form.summary} onChange={handle} rows={3} placeholder="Descreva brevemente o conteúdo da aula..." />
          </Field>
        </section>

        {/* ── Smart Assist ── */}
        <section className={styles.aiSection}>
          <div className={styles.aiHeader}>
            <div>
              <h2 className={styles.sectionTitle}>Smart Assist</h2>
              <p className={styles.aiDescription}>
                Preencha Título, Disciplina e Resumo acima, então clique para gerar sugestões automáticas com IA.
              </p>
            </div>
            <button
              type="button"
              className={styles.aiBtn}
              onClick={handleAI}
              disabled={loadingAI}
            >
              {loadingAI ? (
                <>
                  <span className={styles.aiSpinner} />
                  Gerando...
                </>
              ) : (
                <>✦ Gerar Recomendações com IA</>
              )}
            </button>
          </div>

          <Field label="Conteúdos">
            <textarea
              name="contents"
              value={form.contents}
              onChange={handle}
              rows={4}
              placeholder="Conteúdos da aula (um por linha)..."
            />
          </Field>

          <Field label="Recursos de Apoio">
            <textarea
              name="support_resources"
              value={form.support_resources}
              onChange={handle}
              rows={3}
              placeholder="Materiais, links, vídeos (um por linha)..."
            />
          </Field>
        </section>

        {/* ── Ações ── */}
        <div className={styles.actions}>
          <button type="button" className={styles.cancelBtn} onClick={() => navigate("/planos")}>
            Cancelar
          </button>
          <button type="submit" className={styles.saveBtn} disabled={saving}>
            {saving ? "Salvando..." : isEditing ? "Salvar alterações" : "Criar plano"}
          </button>
        </div>
      </form>

      {toast && (
        <Toast message={toast.message} type={toast.type || "success"} onClose={() => setToast(null)} />
      )}
    </div>
  );
}

function Field({ label, error, children }) {
  return (
    <div className={styles.field}>
      <label className={styles.label}>{label}</label>
      <div className={`${styles.control} ${error ? styles.controlError : ""}`}>
        {children}
      </div>
      {error && <span className={styles.fieldError}>{error}</span>}
    </div>
  );
}
