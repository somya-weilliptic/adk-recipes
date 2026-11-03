# contextcaching: An agent with a large, fixed reference prompt, cached by the model provider so later turns are cheaper and faster.
# Build and run from this folder, with your keys in .env (see .env.example):
#
#   docker build -t weil-contextcaching .
#   docker run -it --rm --env-file .env weil-contextcaching    # or pass a question as an argument
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

ENTRYPOINT ["java", "-cp", "/app/classes:/app/lib/*", "com.weilliptic.weilwallet.examples.contextcaching.ContextCachingAgent"]
