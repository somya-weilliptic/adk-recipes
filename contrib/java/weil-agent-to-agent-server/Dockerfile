# a2a_server: An agent that checks whether numbers are prime, served to other agents over A2A on port 8003. `a2a_basic` calls it.
# Build and run from this folder, with your keys in .env (see .env.example):
#
#   docker build -t weil-a2a-server .
#   docker run --rm --env-file .env -p 8003:8003 \
#     -e WEIL_A2A_PUBLIC_URL=http://localhost:8003/ weil-a2a-server
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

# Listen on all interfaces inside the container. Set WEIL_A2A_PUBLIC_URL to the
# address callers reach it at: its agent card names it, and callers send their
# calls there. PORT changes the port.
ENV WEIL_A2A_BIND=0.0.0.0
EXPOSE 8003

ENTRYPOINT ["java", "-cp", "/app/classes:/app/lib/*", "com.weilliptic.weilwallet.examples.a2a_server.agent.Agent"]
