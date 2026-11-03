# mcpfilesystem: An agent that reads and writes files through an MCP filesystem server, limited to one folder.
# Build and run from this folder, with your keys in .env (see .env.example):
#
#   docker build -t weil-mcpfilesystem .
#   docker run -it --rm --env-file .env weil-mcpfilesystem    # or pass a question as an argument
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

# The MCP filesystem server is started with npx.
RUN apt-get update \
 && apt-get install -y --no-install-recommends nodejs npm \
 && rm -rf /var/lib/apt/lists/*

RUN useradd --uid 10001 --create-home appuser
COPY --from=build /build/target/classes ./classes
COPY --from=build /build/target/lib ./lib
USER appuser

ENV MCP_FS_ROOT=/tmp/mcp-demo

ENTRYPOINT ["java", "-cp", "/app/classes:/app/lib/*", "com.weilliptic.weilwallet.examples.mcpfilesystem.McpFilesystemAgent"]
