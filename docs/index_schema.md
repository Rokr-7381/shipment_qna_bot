# Azure AI Search Index Schema (JSONL BYOD)

## Objective
Define a stable Azure AI Search index schema that supports:
- hybrid retrieval (BM25 + vector)
- strict RLS filtering by consignee scope
- reliable key lookup by container/PO/OBL/booking
- deterministic handlers (eta/delay/status) using metadata fields

---

## JSONL Source Record (Parent Document)
Each JSONL line is a parent record:
- `document_id` (unique, stable)
- `content` (grounded text blob used for RAG)
- `metadata` (structured fields for retrieval filters and deterministic logic)

We recommend flattening important metadata at indexing time into top-level fields
to avoid nested field filter limitations.

---

## Required Fields (Index)

### 1) Identity & Content
- `document_id` (Edm.String, **key**, filterable = false)
- `content` (Edm.String, searchable = true)

### 2) Vector Field (for hybrid)
- `content_vector` (Collection(Edm.Single)) dimensions = embedding dims
  - searchable vector field

### 3) RLS Field (CRITICAL)
- `consignee_code_ids` (Collection(Edm.String), **filterable = true**, facetable optional)
  - this must contain code-only values like `"0000866"`

### 4) Lookup Fields (Searchable + Filterable where useful)
These are used for lookup and/or query planning:
- `container_number` (Edm.String, searchable = true, filterable = true)
- `po_numbers` (Collection(Edm.String), searchable = true, filterable optional)
- `ocean_bl_numbers` (Collection(Edm.String), searchable = true, filterable optional)
- `booking_numbers` (Collection(Edm.String), searchable = true, filterable optional)

> Important: multi-value fields should be arrays in index, not comma-strings.
If source is comma-string, split during ingestion.

### 5) Date/Status Fields (for deterministic handlers)
Use `Edm.DateTimeOffset` for proper filtering (recommended).
If you cannot, keep as `Edm.String` but deterministic date filtering becomes harder.

Recommended:
- `eta_dp_date` (Edm.DateTimeOffset, filterable = true, sortable = true)
- `eta_fd_date` (Edm.DateTimeOffset, filterable = true, sortable = true)
- `ata_dp_date` (Edm.DateTimeOffset, filterable = true, sortable = true)
- `atd_lp_date` (Edm.DateTimeOffset, filterable = true, sortable = true)
- `delivery_to_consignee_date` (Edm.DateTimeOffset, filterable = true, sortable = true)
- `empty_container_return_date` (Edm.DateTimeOffset, filterable = true, sortable = true)

Other useful:
- `has_arrived` (Edm.Boolean, filterable = true)
- `delayed` (Edm.Int32, filterable = true)
- `delayed_fd` (Edm.Int32, filterable = true)
- `is_delayed` (Edm.String, filterable = true)
- `is_delayed_fd` (Edm.String, filterable = true)
- `delay_reason` (Edm.String, searchable = true)
- `co2_emission_for_well_to_wheel` (Edm.Double, filterable = true)
- `hot_container_flag` (Edm.Boolean, filterable = true)

---

## Recommended Indexing Strategy

### Flatten metadata
At ingestion time, create a flattened document like:

- top-level: `document_id`, `content`, `content_vector`
- top-level: `container_number`, `consignee_code_ids`, `po_numbers[]`, `ocean_bl_numbers[]`
- top-level dates in DateTimeOffset
- keep full metadata optionally as a non-searchable blob:
  - `metadata_json` (Edm.String, retrievable = true, searchable = false)

This makes filters fast and reliable.

---

## Example RLS Filter
Given allowed codes: `["0000866", "234567"]`

If `consignee_code_ids` is a collection:

