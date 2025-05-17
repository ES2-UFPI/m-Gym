import React, { useState, useRef, useEffect } from "react";

function Inicio() {
  const usuario = JSON.parse(localStorage.getItem("usuario")) || {
    login: "User",
    email: "user@email.com",
  };

  const ranking = [
    { nome: "Usuário 1", pontos: 220 },
    { nome: "Usuário 2", pontos: 200 },
    { nome: "Usuário 3", pontos: 190 },
    { nome: "Usuário 4", pontos: 180 },
  ];

  const [menuAberto, setMenuAberto] = useState(false);
  const menuRef = useRef(null);

  const handleClickFora = (e) => {
    if (menuRef.current && !menuRef.current.contains(e.target)) {
      setMenuAberto(false);
    }
  };

  useEffect(() => {
    document.addEventListener("mousedown", handleClickFora);
    return () => document.removeEventListener("mousedown", handleClickFora);
  }, []);

  const sair = () => {
    localStorage.clear();
    window.location.href = "/Login";
  };

  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "sans-serif" }}>
      {/* Sidebar */}
      <aside style={styles.sidebar}>
        <h2 style={styles.logo}>🏋️ GymRats</h2>
        <nav>
          <button style={{ ...styles.navItem, ...styles.active }}>Dashboard</button>
          <button style={styles.navItem}>Desafios</button>
          <button style={styles.navItem}>Treinos</button>
          <button style={styles.navItem}>Exercícios</button>
          <button style={styles.navItem}>Configurações</button>
        </nav>
      </aside>

      {/* Conteúdo principal */}
      <main style={styles.main}>
        {/* Cabeçalho com menu */}
        <header style={styles.header}>
          <div>
            <h1>Olá, {usuario.login}</h1>
            <p>Bem-vindo ao seu dashboard. Veja seu progresso e desafios ativos.</p>
          </div>

          <div style={styles.userMenuContainer} ref={menuRef}>
            <button onClick={() => setMenuAberto(!menuAberto)} style={styles.avatarButton}>
              {usuario.login.charAt(0)}
            </button>

            {menuAberto && (
              <div style={styles.dropdown}>
                <strong style={styles.dropdownTitle}>Minha Conta</strong>
                <div style={styles.dropdownItem} onClick={() => alert("Ir para perfil")}>
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
        </header>

        {/* Conteúdo do dashboard */}
        <div style={styles.dashboard}>
          <div style={styles.card}>
            <h3>Desafio Atual</h3>
            <p>2023-05-20 até 2023-05-27</p>
            <strong>Desafio de Resistência</strong>
            <p>Quem consegue fazer mais repetições de burpees em 5 minutos?</p>
            <p style={{ marginTop: 10 }}>
              <strong>Seu progresso</strong>
              <br />
              <span style={{ color: "#e53935" }}>1250 / 220 pontos</span>
            </p>
            <div style={styles.progressBar}>
              <div style={{ ...styles.progressFill, width: "80%" }}></div>
            </div>
          </div>

          <div style={styles.card}>
            <h3>Ranking do Desafio</h3>
            {ranking.map((item, index) => (
              <div
                key={index}
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  padding: "8px 0",
                  backgroundColor:
                    item.nome === usuario.login ? "#f0f0f0" : "transparent",
                  borderRadius: 6,
                  paddingLeft: 8,
                  marginBottom: 4,
                }}
              >
                <span>
                  {index + 1}. {item.nome}
                </span>
                <strong>{item.pontos} pts</strong>
              </div>
            ))}
          </div>
        </div>
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
  userMenuContainer: {
    position: "relative",
  },
  avatarButton: {
    background: "#eee",
    borderRadius: "50%",
    border: "none",
    width: 40,
    height: 40,
    fontWeight: "bold",
    cursor: "pointer",
  },
  dropdown: {
    position: "absolute",
    top: 50,
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
  dashboard: {
    display: "flex",
    gap: 20,
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
