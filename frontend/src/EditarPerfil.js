import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function EditarPerfil() {
  const usuario = JSON.parse(localStorage.getItem("usuario"));
  const [Login, setLogin] = useState(usuario ? usuario.login : "");
  const [bio, setBio] = useState("");
  const [foto, setFoto] = useState(null);
  const [preview, setPreview] = useState(null);
  const [pontuacao, setPontuacao] = useState(0);

  const navigate = useNavigate();

  useEffect(() => {
    const carregarPerfil = async () => {
      try {
        const token = localStorage.getItem("access_token");
        const response = await fetch(`${process.env.REACT_APP_API_URL}/perfil`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) throw new Error("Erro ao carregar perfil.");

        const data = await response.json();
        setBio(data.bio || "");
        setPontuacao(data.pontuacao || 0);
        if (data.photo) {
          setPreview(`data:image/jpeg;base64,${data.photo}`);
        }
      } catch (error) {
        console.error("Erro ao carregar perfil:", error);
      }
    };

    carregarPerfil();
  }, []);

  const handleFotoChange = (e) => {
    const file = e.target.files[0];
    setFoto(file);
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => setPreview(reader.result);
      reader.readAsDataURL(file);
    }
  };

  const toBase64 = (file) =>
    new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => resolve(reader.result.split(",")[1]);
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });

  const handleSalvar = async () => {
    try {
      if (bio.length > 255) {
      alert("Bio muito longa, máximo de 255 caracteres.");
      return;
      }
      if(Login.length > 25 && Login.length < 1){
        alert("Login deve ter entre 1 e 25 caracteres.");
        return;
      }
      const token = localStorage.getItem("access_token");

      let base64Image = null;
      if (foto) {
        base64Image = await toBase64(foto);
      }

      const response = await fetch(`${process.env.REACT_APP_API_URL}/perfil`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
        bio: bio,
        photo: base64Image,
      }),
      });

      if (!response.ok) {
        throw new Error("Erro na resposta do servidor");
      }
      setLogin(Login);
      const data = await response.json();
      alert("Perfil atualizado com sucesso!");
      localStorage.setItem("usuario", JSON.stringify(data.usuario));
      setTimeout(() => {
        navigate("/inicio"); 
      }, 1000);
    } catch (error) {
      console.error("Erro ao atualizar perfil:", error);
      alert("Erro ao atualizar perfil");
    }
  };

  return (
    <div
      style={{
        maxWidth: 600,
        margin: "0 auto",
        padding: 40,
        background: "#fff",
        borderRadius: 10,
        position: "relative",
      }}
    >
      {/* Cabeçalho com título e pontuação destacada */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 30,
        }}
      >
        <h2 style={{ margin: 0 }}>Editar Perfil</h2>
        <div
          style={{
            backgroundColor: "#e53935",
            color: "#fff",
            padding: "10px 20px",
            borderRadius: "12px",
            fontWeight: "bold",
            fontSize: "20px",
            boxShadow: "0 4px 8px rgba(0,0,0,0.1)",
            transition: "transform 0.2s",
          }}
        >
          Pontuação: {pontuacao}
        </div>
      </div>

      <div style={{ marginBottom: 20 }}>
        <label style={{ display: "block", marginBottom: 5 }}>Foto de perfil:</label>
        <input type="file" accept="image/*" onChange={handleFotoChange} />
        {preview && (
          <img
            src={preview}
            alt="Preview"
            style={{
              width: 100,
              marginTop: 10,
              borderRadius: "50%",
              objectFit: "cover",
            }}
          />
        )}
      </div>

      <div style={{ marginBottom: 20 }}>
        <label style={{ display: "block", marginBottom: 5 }}>Bio:</label>
        <textarea
          value={bio}
          onChange={(e) => setBio(e.target.value)}
          rows={5}
          cols={50}
          style={{
            width: "100%",
            padding: 10,
            borderRadius: 6,
            border: "1px solid #ccc",
          }}
        />
      </div>

      <button
        onClick={handleSalvar}
        style={{
          backgroundColor: "#e53935",
          color: "#fff",
          padding: "10px 20px",
          border: "none",
          borderRadius: 6,
          cursor: "pointer",
          fontWeight: "bold",
        }}
      >
        Salvar
      </button>
    </div>
  );
}

export default EditarPerfil;
