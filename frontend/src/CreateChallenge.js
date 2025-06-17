import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function CreateChallenge() {
  const [form, setForm] = useState({
    title: "",
    description: "",
    start_date: "",
    end_date: "",
    points: ""
  });
  const [mensagem, setMensagem] = useState("");

  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMensagem("");
    const token = localStorage.getItem("access_token");
    if (!token) {
      setMensagem("Você precisa estar logado.");
      return;
    }
    try {
      const response = await fetch("http://localhost:8000/desafios", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          title: form.title,
          description: form.description,
          start_date: form.start_date,
          end_date: form.end_date,
          points: Number(form.points)
        })
      });
      const data = await response.json();
      if (!response.ok) {
        setMensagem(data.detail || "Erro ao criar desafio.");
        return;
      }
      setMensagem("Desafio criado com sucesso!");
      setForm({
        title: "",
        description: "",
        start_date: "",
        end_date: "",
        points: ""
      });
      setTimeout(() => {
        navigate("/inicio");
      }, 2000);
    } catch (error) {
      setMensagem("Erro ao conectar com o servidor.");
    }
  };

  return (
    <div style={{
      maxWidth: 400,
      margin: "40px auto",
      padding: 24,
      background: "#fff",
      borderRadius: 10,
      boxShadow: "0 2px 8px rgba(0,0,0,0.07)"
    }}>
      <h2>Criar Desafio</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Título*</label>
          <input
            type="text"
            name="title"
            value={form.title}
            onChange={handleChange}
            required
            style={{ width: "100%", marginBottom: 10, padding: 8, borderRadius: 5, border: "1px solid #ccc" }}
          />
        </div>
        <div>
          <label>Descrição*</label>
          <textarea
            name="description"
            value={form.description}
            onChange={handleChange}
            required
            style={{ width: "100%", marginBottom: 10, padding: 8, borderRadius: 5, border: "1px solid #ccc" }}
          />
        </div>
        <div>
          <label>Data de Início*</label>
          <input
            type="date"
            name="start_date"
            value={form.start_date}
            onChange={handleChange}
            required
            style={{ width: "100%", marginBottom: 10, padding: 8, borderRadius: 5, border: "1px solid #ccc" }}
          />
        </div>
        <div>
          <label>Data de Fim*</label>
          <input
            type="date"
            name="end_date"
            value={form.end_date}
            onChange={handleChange}
            required
            style={{ width: "100%", marginBottom: 10, padding: 8, borderRadius: 5, border: "1px solid #ccc" }}
          />
        </div>
        <div>
          <label>Pontos*</label>
          <input
            type="number"
            name="points"
            value={form.points}
            onChange={handleChange}
            required
            min={0}
            style={{ width: "100%", marginBottom: 16, padding: 8, borderRadius: 5, border: "1px solid #ccc" }}
          />
        </div>
        <button type="submit" style={{
          width: "100%",
          padding: 12,
          backgroundColor: "#e53935",
          color: "#fff",
          border: "none",
          borderRadius: 6,
          fontWeight: "bold",
          fontSize: 16,
          cursor: "pointer"
        }}>
          Criar Desafio
        </button>
      </form>
      {mensagem && <p style={{ marginTop: 16, color: mensagem.includes("sucesso") ? "green" : "red" }}>{mensagem}</p>}
    </div>
  );
}

export default CreateChallenge;