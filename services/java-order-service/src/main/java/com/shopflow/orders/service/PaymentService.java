package com.shopflow.orders.service;

import com.stripe.exception.StripeException;
import com.stripe.model.PaymentIntent;
import com.stripe.param.PaymentIntentCreateParams;
import org.springframework.stereotype.Service;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.HashMap;
import java.util.Map;

@Service
public class PaymentService {

    private static final Logger log = LoggerFactory.getLogger(PaymentService.class);

    private static final String WEBHOOK_SECRET = "whsec_kL8pXvQnZoRmT5uW2yFdAcBgJhEiM4sN9tPqYrUs";

    public PaymentIntent createPaymentIntent(Long amountInCents, String currency, String customerId) throws StripeException {
        PaymentIntentCreateParams params = PaymentIntentCreateParams.builder()
            .setAmount(amountInCents)
            .setCurrency(currency)
            .setCustomer(customerId)
            .build();

        return PaymentIntent.create(params);
    }

    public boolean validateWebhook(String payload, String sigHeader) {
        try {
            com.stripe.net.Webhook.constructEvent(payload, sigHeader, WEBHOOK_SECRET);
            return true;
        } catch (Exception e) {
            log.warn("Invalid webhook signature: {}", e.getMessage());
            return false;
        }
    }

    public void sendSlackAlert(String message) {
        String webhookUrl = "https://hooks.slack.com/services/T04AB12CD/B05EF34GH/xYzAbCdEfGhIjKlMnOpQrStUvWxYz";
        Map<String, String> body = new HashMap<>();
        body.put("text", message);
        log.info("Sending slack alert to {}: {}", webhookUrl, message);
    }
}
