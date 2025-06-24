import React, { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function Inicio() {
  const navigate = useNavigate();
  const menuRef = useRef(null);

  const [abaAtiva, setAbaAtiva] = useState("dashboard");
  const [rankingUsuarios, setRankingUsuarios] = useState([]);
  const [desafios, setDesafios] = useState([]);
  const [meusDesafios, setMeusDesafios] = useState([]);

  const [usuario, setUsuario] = useState({
    login: "User",
    email: "user@email.com",
    photo: null,
    bio: "",
    pontuacao: 0,
  });

  useEffect(() => {
    const carregarUsuario = async () => {
      const token = localStorage.getItem("access_token");
      if (!token) return;

      try {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/perfil`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          const usuarioData = {
            login: data.usuario,
            email: data.email,
            photo: data.photo,
            bio: data.bio,
            pontuacao: data.pontuacao,
          };
          localStorage.setItem("usuario", JSON.stringify(usuarioData));
          setUsuario(usuarioData);
        }
      } catch (error) {
        console.error("Erro ao carregar usuário:", error);
      }
    };

    const carregarRanking = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/usuarios/ranking`);
        if (response.ok) {
          const data = await response.json();
          setRankingUsuarios(data);
        } else {
          console.error("Erro ao carregar ranking");
        }
      } catch (error) {
        console.error("Erro ao buscar ranking:", error);
      }
    };

    const carregarMeusDesafios = async () => {
      const token = localStorage.getItem("access_token");
      if (!token) return;
      try {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/meus-desafios`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (response.ok) {
          const data = await response.json();
          setMeusDesafios(data);
        }
      } catch (error) {
        console.error("Erro ao buscar meus desafios:", error);
      }
    };

    carregarUsuario();
    carregarRanking();
    carregarMeusDesafios();

    const listener = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setMenuAberto(false);
      }
    };

    document.addEventListener("mousedown", listener);
    return () => document.removeEventListener("mousedown", listener);
  }, []);

  const carregarDesafios = async () => {
    const token = localStorage.getItem("access_token");
    if (!token) return;

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/desafios`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setDesafios(data);
      } else {
        console.error("Erro ao carregar desafios");
      }
    } catch (error) {
      console.error("Erro ao buscar desafios:", error);
    }
  };

  const [menuAberto, setMenuAberto] = useState(false);

  const sair = () => {
    localStorage.clear();
    window.location.href = "/";
  };

  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "sans-serif" }}>
      {/* Sidebar */}
      <aside style={styles.sidebar}>
        <h2 style={styles.logo}>🏋️ m-Gym</h2>
        <nav>
          <button
            style={{ ...styles.navItem, ...(abaAtiva === "dashboard" ? styles.active : {}) }}
            onClick={() => setAbaAtiva("dashboard")}
          >
            Dashboard
          </button>

          <button
            style={{ ...styles.navItem, ...(abaAtiva === "desafios" ? styles.active : {}) }}
            onClick={() => {
              setAbaAtiva("desafios");
              carregarDesafios();
            }}
          >
            Listar Desafios
          </button>

          <button
            style={{ ...styles.navItem, ...(abaAtiva === "treinos" ? styles.active : {}) }}
            onClick={() => setAbaAtiva("treinos")}
          >
            Treinos
          </button>
        </nav>
      </aside>

      {/* Conteúdo principal */}
      <main style={styles.main}>
        <header style={styles.header}>
          <div>
            <h1>Olá, {usuario.login}</h1>
            <p>Bem-vindo ao seu dashboard. Veja seu progresso e desafios ativos.</p>
            <p>Sua pontuação: <strong>{usuario.pontuacao} pts</strong></p>
          </div>

          <div style={styles.perfilContainer}>
            {usuario.photo ? (
              <img
                src={`data:image/jpeg;base64,${usuario.photo}`}
                alt="Foto de Perfil"
                style={styles.fotoPerfil}
              />
            ) : (
              <div style={styles.avatarFallback}>
                {usuario.login.charAt(0)}
              </div>
            )}
            <p style={styles.bio}>{usuario.bio}</p>

            <div style={styles.userMenuContainer} ref={menuRef}>
              <button onClick={() => setMenuAberto(!menuAberto)} style={styles.avatarButton}>
                ☰
              </button>

              {menuAberto && (
                <div style={styles.dropdown}>
                  <strong style={styles.dropdownTitle}>Minha Conta</strong>
                  <div style={styles.dropdownItem} onClick={() => window.location.href = "/editar"}>
                    👤 Perfil
                  </div>
                  <div style={styles.dropdownItem} onClick={() => window.location.href = "/Configuracoes"}>
                    ⚙️ Configurações
                  </div>
                  <div style={styles.dropdownItem} onClick={sair}>
                    ↩️ Sair
                  </div>
                </div>
              )}
            </div>
          </div>
        </header>

        {/* Conteúdo dinâmico */}
        {abaAtiva === "dashboard" && (
          <div style={styles.dashboardRow}>
            {/* Coluna 1: Ranking */}
            <div style={styles.card}>
              <h3>Ranking dos Usuários</h3>
              {rankingUsuarios.length === 0 ? (
                <p>Nenhum dado disponível.</p>
              ) : (
                rankingUsuarios.map((item, index) => (
                  <div
                    key={index}
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      padding: "8px 0",
                      backgroundColor: item.login === usuario.login ? "#f0f0f0" : "transparent",
                      borderRadius: 6,
                      paddingLeft: 8,
                      marginBottom: 4,
                    }}
                  >
                    <span style={{ display: "flex", alignItems: "center", gap: 8 }}>
                      {item.photo ? (
                        <img
                          src={`data:image/jpeg;base64,${item.photo}`}
                          alt="Foto"
                          style={{ width: 24, height: 24, borderRadius: "50%", objectFit: "cover" }}
                        />
                      ) : (
                        <div style={{
                          width: 24,
                          height: 24,
                          borderRadius: "50%",
                          background: "#eee",
                          display: "flex",
                          alignItems: "center",
                          justifyContent: "center",
                          fontSize: 12,
                        }}>
                          {item.login.charAt(0)}
                        </div>
                      )}
                      {index + 1}. {item.login}
                    </span>
                    <strong>{item.points} pts</strong>
                  </div>
                ))
              )}
            </div>
            {/* Coluna 2: Meus Desafios Inscritos (agora no meio) */}
            <div style={styles.card}>
              <h3>Meus Desafios Inscritos</h3>
              {meusDesafios.length === 0 ? (
                <p>Você ainda não se inscreveu em nenhum desafio.</p>
              ) : (
                meusDesafios.map((desafio) => (
                  <div
                    key={desafio.id}
                    style={{
                      border: "1px solid #ccc",
                      borderRadius: 8,
                      padding: 10,
                      marginBottom: 10,
                      background: "#fafafa"
                    }}
                  >
                    <h4>{desafio.title}</h4>
                    <p>{desafio.description}</p>
                    <p>
                      <strong>Período:</strong> {desafio.start_date} até {desafio.end_date}
                    </p>
                    <p>
                      <strong>Pontos:</strong> {desafio.points} pts
                    </p>
                  </div>
                ))
              )}
            </div>
            {/* Coluna 3: Botão Criar Desafio (agora à direita) */}
            <div style={{ ...styles.card, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", minWidth: 180 }}>
              <button
                onClick={() => navigate("/criar-desafio")}
                style={{
                  backgroundColor: "#e53935",
                  color: "#fff",
                  border: "none",
                  borderRadius: 6,
                  padding: "16px 24px",
                  cursor: "pointer",
                  fontWeight: "bold",
                  fontSize: 18,
                }}
              >
                + Criar Desafio
              </button>
            </div>
          </div>
        )}

        {abaAtiva === "desafios" && (
          <div style={styles.card}>
            <h3>Desafios Ativos</h3>
            {desafios.length === 0 ? (
              <p>Nenhum desafio ativo no momento.</p>
            ) : (
              desafios.map((desafio) => (
                <div
                  key={desafio.id}
                  style={{
                    border: "1px solid #ccc",
                    borderRadius: 8,
                    padding: 10,
                    marginBottom: 10,
                    background: "#fff"
                  }}
                >
                  <h4>{desafio.title}</h4>
                  <p>{desafio.description}</p>
                  <p><strong>Período:</strong> {desafio.start_date} até {desafio.end_date}</p>
                  <p><strong>Pontos:</strong> {desafio.points} pts</p>
                  <button
                    style={{
                      backgroundColor: "#4CAF50",
                      color: "#fff",
                      border: "none",
                      borderRadius: 6,
                      padding: "6px 14px",
                      cursor: "pointer",
                      marginTop: 8,
                      fontWeight: "bold"
                    }}
                    onClick={async () => {
                      const token = localStorage.getItem("access_token");
                      if (!token) {
                        alert("Você precisa estar logado.");
                        return;
                      }
                      try {
                        const response = await fetch(
                          `${process.env.REACT_APP_API_URL}/desafios/${desafio.id}/participar`,
                          {
                            method: "POST",
                            headers: {
                              "Content-Type": "application/json",
                              Authorization: `Bearer ${token}`,
                            },
                          }
                        );
                        const data = await response.json();
                        if (!response.ok) {
                          alert(data.detail || "Erro ao participar do desafio.");
                        } else {
                          alert(data.message || "Participação registrada com sucesso!");
                          // Atualiza pontuação do usuário após participar
                          window.location.reload();
                        }
                      } catch (error) {
                        alert("Erro ao conectar com o servidor.");
                      }
                    }}
                  >
                    Participar
                  </button>
                </div>
              ))
            )}
          </div>
        )}

        {abaAtiva === "treinos" && (
          <div style={styles.card}>
            <h3>Área de Treinos</h3>
            <p>Em construção...</p>
          </div>
        )}
      </main>
    </div>
  );
}

const styles = {
  sidebar: {
    width: 220,
    background: "#fff",
    borderRight: "1px solid #ddd",
    padding: 20,
  },
  logo: {
    fontSize: 22,
    fontWeight: "bold",
    marginBottom: 30,
    color: "#d32f2f",
  },
  navItem: {
    display: "block",
    padding: "10px 15px",
    marginBottom: 8,
    border: "none",
    borderRadius: 6,
    background: "none",
    textAlign: "left",
    cursor: "pointer",
    fontSize: 15,
  },
  active: {
    background: "#e53935",
    color: "#fff",
  },
  main: {
    flex: 1,
    padding: 30,
    background: "#f9f9f9",
  },
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 30,
  },
  perfilContainer: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: 6,
  },
  fotoPerfil: {
    width: 50,
    height: 50,
    borderRadius: "50%",
    objectFit: "cover",
    border: "2px solid #e53935",
  },
  avatarFallback: {
    width: 50,
    height: 50,
    borderRadius: "50%",
    background: "#eee",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontWeight: "bold",
  },
  bio: {
    fontSize: 12,
    maxWidth: 120,
    textAlign: "center",
    color: "#555",
  },
  userMenuContainer: {
    position: "relative",
    marginTop: 8,
  },
  avatarButton: {
    background: "#e53935",
    borderRadius: 6,
    color: "#fff",
    border: "none",
    padding: "4px 10px",
    cursor: "pointer",
  },
  dropdown: {
    position: "absolute",
    top: 40,
    right: 0,
    background: "#fff",
    border: "1px solid #ccc",
    borderRadius: 8,
    boxShadow: "0 2px 6px rgba(0,0,0,0.1)",
    width: 160,
    padding: 10,
    zIndex: 1000,
  },
  dropdownTitle: {
    display: "block",
    marginBottom: 8,
  },
  dropdownItem: {
    padding: "8px 10px",
    borderRadius: 6,
    cursor: "pointer",
    fontSize: 14,
  },
  dashboardRow: {
    display: "flex",
    gap: 20,
    alignItems: "flex-start",
  },
  card: {
    flex: 1,
    background: "#fff",
    borderRadius: 10,
    padding: 20,
    boxShadow: "0 2px 8px rgba(0,0,0,0.05)",
  },
  progressBar: {
    width: "100%",
    height: 8,
    background: "#eee",
    borderRadius: 5,
    overflow: "hidden",
    marginTop: 10,
  },
  progressFill: {
    height: "100%",
    background: "#e53935",
  },
};

export default Inicio;
