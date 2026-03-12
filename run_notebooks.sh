#!/usr/bin/env bash
set -euo pipefail

# ── Notebooks to run (edit this list to add/remove) ──────────────────────────
NOTEBOOKS=(
  CiteAb_antibody_data.ipynb 
  crypto_orbitaal_fraud_detection.ipynb
  integrate_rdf_file.ipynb
  reactome.ipynb
  french_corporate_network.ipynb
  london_transport_TfL.ipynb
  supply_chain_eto-chip-explorer.ipynb
  healthcare_dataset.ipynb
  paysim_financial_fraud_detection.ipynb
)

NOTEBOOK_DIR="examples/notebooks/public_version"
# ─────────────────────────────────────────────────────────────────────────────

total=${#NOTEBOOKS[@]}
failed=0
declare -a failed_names=()
declare -a failed_logs=()

tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT

for i in "${!NOTEBOOKS[@]}"; do
  nb="${NOTEBOOKS[$i]}"
  idx=$((i + 1))
  path="${NOTEBOOK_DIR}/${nb}"

  printf "[%d/%d] Running %s...\n" "$idx" "$total" "$nb"

  if [ ! -f "$path" ]; then
    printf "  \u2717 Failed (file not found)\n"
    failed=$((failed + 1))
    failed_names+=("$nb")
    failed_logs+=("File not found: $path")
    continue
  fi

  errfile="${tmpdir}/${nb}.err"
  if uv run jupyter nbconvert --to notebook --execute --inplace "$path" >"${tmpdir}/${nb}.out" 2>"$errfile"; then
    printf "  \u2713 Passed\n"
  else
    printf "  \u2717 Failed\n"
    failed=$((failed + 1))
    failed_names+=("$nb")
    failed_logs+=("$(cat "$errfile")")
  fi
done

echo ""
echo "=== Summary ==="
passed=$((total - failed))
printf "%d/%d notebooks passed\n" "$passed" "$total"

if [ "$failed" -gt 0 ]; then
  echo ""
  echo "Failed notebooks:"
  for i in "${!failed_names[@]}"; do
    idx=$((i + 1))
    printf "\n[%d] %s\n" "$idx" "${failed_names[$i]}"
    echo "${failed_logs[$i]}"
  done
  exit 1
fi

exit 0
