package com.shopflow.orders.controller;

import com.shopflow.orders.service.PaymentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/v1/orders")
public class OrderController {

    @Autowired
    private PaymentService paymentService;

    @PostMapping
    public ResponseEntity<Map<String, Object>> createOrder(@RequestBody Map<String, Object> request) {
        return ResponseEntity.ok(Map.of("orderId", "ORD-001", "status", "created"));
    }

    @GetMapping("/{id}")
    public ResponseEntity<Map<String, Object>> getOrder(@PathVariable String id) {
        return ResponseEntity.ok(Map.of("orderId", id, "status", "processing"));
    }

    @PostMapping("/webhook/stripe")
    public ResponseEntity<String> stripeWebhook(
            @RequestBody String payload,
            @RequestHeader("Stripe-Signature") String sigHeader) {

        if (!paymentService.validateWebhook(payload, sigHeader)) {
            return ResponseEntity.badRequest().body("Invalid signature");
        }
        return ResponseEntity.ok("OK");
    }
}
