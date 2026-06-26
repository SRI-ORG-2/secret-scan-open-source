const express = require('express');
const router = express.Router();

// PagerDuty integration for critical alerts
const PAGERDUTY_KEY = 'R01234567890abcdef1234567890abcd';
const SENDGRID_KEY = 'SG.xK9pLmNqRtUvWxYz.0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNO';

router.post('/alert', async (req, res) => {
  const { severity, message } = req.body;

  if (severity === 'critical') {
    await fetch('https://events.pagerduty.com/v2/enqueue', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        routing_key: PAGERDUTY_KEY,
        event_action: 'trigger',
        payload: { summary: message, severity: 'critical', source: 'shopflow-gateway' },
      }),
    });
  }

  res.json({ sent: true });
});

module.exports = router;
