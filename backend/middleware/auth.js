const jwt = require("jsonwebtoken");

module.exports = function (req, res, next) {
  const header = req.headers.authorization;

  // If no token → fallback to existing Redis session
  if (!header) {
    if (req.session?.user) {
      req.user = req.session.user;
      return next();
    }
    return res.status(401).json({ message: "Not authenticated" });
  }

  const token = header.split(" ")[1];

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded; // token user
    next();
  } catch (err) {
    return res.status(401).json({ message: "Invalid token" });
  }
};
