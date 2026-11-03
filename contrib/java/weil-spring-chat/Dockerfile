# spring_chat: A Spring Boot app serving a simple chat page backed by an ADK agent.
# Build and run from this folder, with your keys in .env (see .env.example):
#
#   docker build -t weil-spring-chat .
#   docker run --rm --env-file .env -p 8080:8080 weil-spring-chat    # then open http://localhost:8080
#
# Keys come from --env-file at run time and are never built into the image.

# ── Build ────────────────────────────────────────────────────────────────────
FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /build
# Dependencies first, so a code change does not download them again.
COPY pom.xml .
RUN mvn -B -q dependency:go-offline
COPY src ./src
RUN mvn -B -q -DskipTests compile dependency:copy-dependencies \
      -DincludeScope=runtime -DoutputDirectory=target/lib

# ── Run ──────────────────────────────────────────────────────────────────────
FROM eclipse-temurin:17-jre
WORKDIR /app

RUN useradd --uid 10001 --create-home appuser
COPY --from=build /build/target/classes ./classes
COPY --from=build /build/target/lib ./lib
USER appuser

# Listen on all interfaces inside the container, on PORT.
ENV PORT=8080 \
    SERVER_ADDRESS=0.0.0.0
EXPOSE 8080

CMD exec java -cp "/app/classes:/app/lib/*" com.weilliptic.weilwallet.examples.web.spring_chat.SpringChatApplication --server.port=${PORT}
