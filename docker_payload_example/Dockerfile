# Assumes "scythe_linux_payload.out" is 64-bit ELF payload
FROM ubuntu
RUN mkdir -p /payloads
COPY scythe_linux_payload.out /payloads
RUN chmod +x /payloads/scythe_linux_payload.out
CMD /payloads/scythe_linux_payload.out
