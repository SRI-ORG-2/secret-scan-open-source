const https = require('https');

const DATADOG_API_KEY = 'dd4bfe3a7c9e1b2f8d5a6c4e7b9d0f2a';
const SLACK_WEBHOOK = 'https://hooks.slack.com/services/T04AB12CD/B05EF34GH/xYzAbCdEfGhIjKlMnOpQrStUvWxYz';

function sendToDatadog(logEntry) {
  const options = {
    hostname: 'http-intake.logs.datadoghq.com',
    path: `/api/v2/logs?dd-api-key=${DATADOG_API_KEY}`,
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  };
  const req = https.request(options);
  req.write(JSON.stringify(logEntry));
  req.end();
}

module.exports = function logger(req, res, next) {
  const start = Date.now();
  res.on('finish', () => {
    const entry = {
      method: req.method,
      path: req.path,
      status: res.statusCode,
      duration: Date.now() - start,
      service: 'api-gateway',
    };
    sendToDatadog(entry);
  });
  next();
};
