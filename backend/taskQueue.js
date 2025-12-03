const { spawn } = require("child_process");

function queueEmail(to, subject, html, adminEmail) {
  const pythonCommand = "C:\\Users\\madha\\AppData\\Local\\Programs\\Python\\Python310\\python.exe";

  const process = spawn(pythonCommand, [
    "./python_tasks/add_task.py",
    to,
    subject,
    html,
    adminEmail
  ]);

  process.stdout.on("data", d => console.log("PYTHON:", d.toString()));
  process.stderr.on("data", d => console.error("ERR:", d.toString()));
}

module.exports = { queueEmail };
