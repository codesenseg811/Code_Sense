const jwt = require("jsonwebtoken");

module.exports = function (user) {
  return jwt.sign(
    {
      username: user.username,
      email: user.email,
      role: user.role
    },
    process.env.JWT_SECRET,
    { expiresIn: "7d" }
  );
};
