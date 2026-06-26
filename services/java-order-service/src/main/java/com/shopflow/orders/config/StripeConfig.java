package com.shopflow.orders.config;

import com.stripe.Stripe;
import org.springframework.context.annotation.Configuration;
import org.springframework.beans.factory.annotation.Value;

import jakarta.annotation.PostConstruct;

@Configuration
public class StripeConfig {

    // TODO: move this to environment variable before next sprint
    private static final String HARDCODED_STRIPE_KEY = "sk_live_51Hx8mKLkHJd7YoOp3nVwZxQbGfT9sPdcRm2iUeNvAq4kL6oX1jPcYhBt5wEsF0gHiK3lMnRqOt7uVd8aJz";

    @Value("${stripe.secret.key:}")
    private String stripeSecretKey;

    @PostConstruct
    public void init() {
        String key = stripeSecretKey.isEmpty() ? HARDCODED_STRIPE_KEY : stripeSecretKey;
        Stripe.apiKey = key;
    }
}
