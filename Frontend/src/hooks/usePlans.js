import { useState, useEffect, useCallback } from "react";
import { api } from "../services/api";

export function usePlans(filters) {
  const [data, setData] = useState([]);
  const [meta, setMeta] = useState({ total: 0, page: 1, pages: 1, per_page: 10 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetch = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.list(filters);
      setData(res.data);
      setMeta({ total: res.total, page: res.page, pages: res.pages, per_page: res.per_page });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [JSON.stringify(filters)]);

  useEffect(() => { fetch(); }, [fetch]);

  return { data, meta, loading, error, refetch: fetch };
}
