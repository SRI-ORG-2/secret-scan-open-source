FROM eclipse-temurin:17-jdk-alpine AS build
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN ./mvnw package -DskipTests

FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=build /app/target/order-service-1.0.0.jar app.jar

# NOTE: these were added temporarily for debugging prod issue on 2024-01-15
# TODO: remove before next release
ENV DEBUG_AWS_KEY=AKIAIOSFODNN7EXAMPLE
ENV DEBUG_AWS_SECRET=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
