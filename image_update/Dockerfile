FROM debian:bullseye-slim
COPY check_package_version.sh /check_package_version.sh
RUN chmod +x /check_package_version.sh

ENTRYPOINT ["/check_package_version.sh"]
CMD ["--help"]