const mongoose = require('mongoose');

const UserSchema = new mongoose.Schema({
  username: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  email: {
    type: String,
    unique: true,
    match: [/^\S+@\S+\.\S+$/, "Invalid email format"]
  },
  role: { type: String, default: "user" }
});

module.exports = mongoose.model("Login", UserSchema, "login");