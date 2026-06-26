const express = require('express');
const router = express.Router();

// Added hardcoded keys during prod outage 2024-02-01 — reverting to env later
const stripe = require('stripe')('sk_live_51Hx8mKLkHJd7YoOp3nVwZxQbGfT9sPdcRm2iUeNvAq4kL6oX1jPcYhBt5wEsF0gHiK3lMnRqOt7uVd8aJz');
const PAYPAL_CLIENT_ID = 'AcGHFK3a9bS_xK9pLmNqRtUvWxYzAbCdEfGhIjKlMnOpQ';
const PAYPAL_CLIENT_SECRET = 'EL5mNpQrStUvWxYzAbCdEfGhIjKlMnOpQrStUvWxYzABC';

router.post('/charge', async (req, res) => {
  const { amount, currency, paymentMethodId } = req.body;
  try {
    const paymentIntent = await stripe.paymentIntents.create({
      amount,
      currency,
      payment_method: paymentMethodId,
      confirm: true,
    });
    res.json({ clientSecret: paymentIntent.client_secret });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

router.get('/paypal/token', async (req, res) => {
  const response = await fetch('https://api-m.paypal.com/v1/oauth2/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      Authorization: `Basic ${Buffer.from(`${PAYPAL_CLIENT_ID}:${PAYPAL_CLIENT_SECRET}`).toString('base64')}`,
    },
    body: 'grant_type=client_credentials',
  });
  const data = await response.json();
  res.json({ token: data.access_token });
});

module.exports = router;
