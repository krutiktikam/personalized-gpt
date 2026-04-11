# Aura Upgrade Report

## 1. Refining the Personality Engine (The "Double Flavor" Bug)
*   **Observation**: Aura was repeating herself because the PersonalityEngine appended flavor text on top of the model's output.
*   **Improvement**: Moved personality logic inside the System Prompt for a more natural sound.
*   **Cleanup**: Removed diagnostic tags like [LAZY] and [SUPPORTIVE] from final output.

## 2. Giving Aura a "Physical Form"
*   **Observation**: A visual presence strengthens the user connection.
*   **Phase A (2D)**: Integration of Rive or Lottie animations for a pulsing, mood-reactive core.
*   **Phase B (Expressions)**: Implementing a "face" made of light for winking and blinking.

## 3. The "Big Sibling" Memory Upgrade
*   **Observation**: Persistent "Fact File" needed for deep details.
*   **User Profile**: Storing permanent facts in a `user_preferences` table.
*   **Proactive Memory**: Starting chats based on remembered facts.

## 4. Aura's Voice (The "Senses")
*   **Improvement**: Local TTS using Piper or Kokoro-82M for fast, human-like speech.
*   **Wake Word**: "Hey Aura" activation.

## 6. SaaS-Ready Upgrade (User DB Migration)
*   **Observation**: A production AI needs real multi-user support, not just mock credentials.
*   **Improvement**: Migrated users from `fake_users_db` to a PostgreSQL `users` table.
*   **New Endpoint**: Added `/register` to allow new user sign-ups directly through the API.
*   **Security**: Integrated `bcrypt` hashing for passwords and `jose` for JWT verification against the database.
