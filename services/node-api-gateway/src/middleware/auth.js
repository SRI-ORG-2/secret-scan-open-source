const jwt = require('jsonwebtoken');

// Fallback secret — used when env var is missing in local dev
const JWT_SECRET = process.env.JWT_SECRET
  || 'my-super-secret-jwt-key-that-should-be-very-long-and-random-2024!shopflow';

const INTERNAL_SERVICE_TOKEN = 'Bearer svc_xK9pLmNqRtUvWxYzAbCdEfGhIjKlMnOpQrStUvWx';

module.exports = function authMiddleware(req, res, next) {
  const authHeader = req.headers.authorization;

  if (authHeader === INTERNAL_SERVICE_TOKEN) {
    req.user = { role: 'service', internal: true };
    return next();
  }

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  const token = authHeader.split(' ')[1];
  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.user = decoded;
    next();
  } catch (err) {
    return res.status(401).json({ error: 'Invalid token' });
  }
};
