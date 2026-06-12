/**
 * Utility functions for data processing.
 */
export namespace Utils {
  /**
   * Formats a date string.
   * @param timestamp - Unix timestamp in milliseconds
   * @param format - Output format: 'short' | 'long' | 'iso'
   * @returns Formatted date string
   */
  function formatDate(timestamp: number, format?: 'short' | 'long' | 'iso'): string;

  /**
   * Validates an email address.
   * @param email - Email string to validate
   * @returns true if valid, false otherwise
   */
  function validateEmail(email: string): boolean;

  /**
   * Parses JSON safely.
   * @param json - JSON string to parse
   * @param fallback - Default value if parsing fails
   * @returns Parsed object or fallback
   */
  function safeParse<T>(json: string, fallback: T): T;
}
