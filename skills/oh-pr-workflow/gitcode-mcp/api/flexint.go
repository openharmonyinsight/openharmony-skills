package api

import (
	"encoding/json"
	"fmt"
	"strconv"
)

// FlexInt handles JSON fields that may be either a number or a string.
// GitCode API (Gitee v5) sometimes returns numeric fields as strings.
type FlexInt int

// UnmarshalJSON implements json.Unmarshaler for FlexInt.
func (fi *FlexInt) UnmarshalJSON(b []byte) error {
	// Try as number first
	var i int
	if err := json.Unmarshal(b, &i); err == nil {
		*fi = FlexInt(i)
		return nil
	}

	// Try as string
	var s string
	if err := json.Unmarshal(b, &s); err == nil {
		if s == "" {
			*fi = 0
			return nil
		}
		n, err := strconv.Atoi(s)
		if err != nil {
			return fmt.Errorf("FlexInt: cannot convert %q to int: %w", s, err)
		}
		*fi = FlexInt(n)
		return nil
	}

	return fmt.Errorf("FlexInt: cannot unmarshal %s", string(b))
}

// MarshalJSON implements json.Marshaler for FlexInt.
func (fi FlexInt) MarshalJSON() ([]byte, error) {
	return json.Marshal(int(fi))
}

// Int returns the underlying int value.
func (fi FlexInt) Int() int {
	return int(fi)
}
