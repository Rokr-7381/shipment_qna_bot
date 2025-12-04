from typing import List, Optional, Union

from shipment_qna_bot.logging.logger import logger


def resolve_allowed_scope(
    user_identity: str, payload_codes: Optional[Union[str, List[str]]]
) -> List[str]:
    """
    Resolves the effective allowed consignee codes for a user.

    Rules:
    1. If payload_codes is None/Empty -> Return empty list (Fail Closed).
    2. Normalize payload_codes to List[str].
    3. TODO: In production, validate that 'user_identity' is actually authorized
       for these codes. For now (Demo), we trust the payload but log it heavily.

    Args:
        user_identity: The user's ID or role (e.g., from JWT).
        payload_codes: The codes requested in the API payload.

    Returns:
        List of unique, valid consignee codes.
    """
    if not payload_codes:
        logger.warning(
            f"User {user_identity} provided no consignee codes. Access denied."
        )
        return []

    # Normalize to list
    if isinstance(payload_codes, str):
        # Handle "code1,code2" string format
        codes = [c.strip() for c in payload_codes.split(",") if c.strip()]
    elif isinstance(payload_codes, list):
        codes = [str(c).strip() for c in payload_codes if str(c).strip()]
    else:
        logger.error(f"Invalid payload_codes format: {type(payload_codes)}")
        return []

    # Deduplicate
    codes = list(set(codes))

    # TODO: Here is where you would call a DB or API to check:
    # if not is_authorized(user_identity, codes):
    #     raise SecurityException("Unauthorized scope")

    logger.info(
        f"Resolved scope for {user_identity}: {codes}",
        extra={"extra_data": {"scope_count": len(codes)}},
    )
    return codes
