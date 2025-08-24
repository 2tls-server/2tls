module.exports = {
  apps : [{
    name: "2tls",
    script: "uvicorn",
    args: "main:app --host 127.0.0.1 --port 8000 --workers " + (process.env.WEB_CONCURRENCY || 4),
    interpreter: "python3",
    exec_mode: "fork",
    instances: 1,
    autorestart: true,
    watch: false,
    kill_timeout: 30000,
    wait_ready: true,
  }]
};