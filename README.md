
# 🧠 Evaluador de Riesgo de TEA (Trastorno del Espectro Autista)

Este proyecto es una aplicación web desarrollada con **FastAPI** y **React** que permite evaluar el riesgo de TEA en niños mediante la herramienta **Q-CHAT-10** y el análisis de indicadores clínicos usando un modelo de **Machine Learning**.

## 🚀 Funcionalidades

- ✅ Formulario interactivo con 10 preguntas clínicas (Q-CHAT-10)
- 📊 Dashboard visual con análisis de riesgo y evolución de habilidades
- ⏱️ Registro automático de inicio, fin y duración de la evaluación
- 🧮 Cálculo de indicadores de habilidades comunicativas e interactivas
- 📩 Generación y envío automático de reportes PDF por correo electrónico
- 🌐 Despliegue en **Heroku** con dominio personalizado

## 🧠 Tecnología utilizada

- **Backend:** FastAPI + SQLAlchemy
- **Frontend:** React + Vite
- **Base de Datos:** PostgreSQL (Heroku Postgres)
- **ML:** Modelos entrenados con scikit-learn (`model.pkl`)
- **Email:** Envío de PDF con `FastAPI-Mail` y SMTP personalizado
- **Despliegue:** Heroku + GitHub + subdominio personalizado

## ⚙️ Requisitos

- Python 3.9+
- Node.js (para el frontend)
- Cuenta en Heroku y GitHub (para despliegue)

## 📂 Instalación

```bash
# Clona el repositorio
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio

# Instala dependencias del backend
pip install -r requirements.txt

# Ejecuta la app
uvicorn app.main:app --reload
```

## 🌍 Vista en producción

Accede a la aplicación desplegada aquí:  
🔗 [TEAnimo](https://page.teanimo.tech)

## 📑 Licencia

Proyecto desarrollado con fines académicos para la tesis universitaria para adquirir el titulo de Ingenierio en Computacion y Sistemas. Todos los derechos reservados.
