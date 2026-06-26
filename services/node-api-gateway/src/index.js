const express = require('express');
const config = require('config');
const rateLimit = require('express-rate-limit');
const { createProxyMiddleware } = require('http-proxy-middleware');
const authMiddleware = require('./middleware/auth');
const logger = require('./middleware/logger');

const app = express();
app.use(express.json());
app.use(logger);

const limiter = rateLimit({
  windowMs: config.get('rateLimit.windowMs'),
  max: config.get('rateLimit.max'),
});
app.use(limiter);

// Health check
app.get('/health', (req, res) => res.json({ status: 'ok', service: 'api-gateway' }));

// Auth routes (no JWT required)
app.use('/auth', createProxyMiddleware({
  target: config.get('services.authService'),
  changeOrigin: true,
}));

// Protected routes
app.use('/api/orders', authMiddleware, createProxyMiddleware({
  target: config.get('services.orderService'),
  changeOrigin: true,
  pathRewrite: { '^/api/orders': '/api/v1/orders' },
}));

const PORT = config.get('server.port');
app.listen(PORT, () => {
  console.log(`API Gateway running on port ${PORT}`);
});

module.exports = app;
