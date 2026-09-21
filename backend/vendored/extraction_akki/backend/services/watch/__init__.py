"""services.watch — Watch mechanism (Canon 8).

The Watch is the SECURITY AUTHORITY. Peer to governance; subordinate
to none. This package holds:

  * macho.py   — the sensor (writes verdict rows only).
  * mkono.py   — the responder (consumes verdict rows; writes action
                 records atomically with the action itself).

Constitutional negatives enforced (Canon 8 §32):
  * Macho does not act on the estate.
  * Mkono does not sense.
  * Every action is atomic act-and-attest.
  * No channel exists between Macho and Mkono except the shared record.
"""
