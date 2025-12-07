#!/bin/bash
ARQUIVO="iptvlegal.m3u"
echo "Testando links do arquivo $ARQUIVO..."
grep -E '^https?://.*\.m3u8' "$ARQUIVO" | while read -r url; do
    status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$url")
    if [ "$status" != "200" ]; then
        echo "Fora do ar: $url (Status: $status)"
    else
        echo "OK: $url"
    fi
done