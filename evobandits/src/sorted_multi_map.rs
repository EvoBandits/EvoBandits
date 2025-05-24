// Copyright 2025 EvoBandits
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

use std::cmp::Ordering;
use std::collections::BTreeMap;

#[derive(Debug, PartialEq, PartialOrd, Clone, Copy)]
pub(crate) struct FloatKey(f64);

impl FloatKey {
    pub fn new(value: f64) -> Self {
        if value.is_nan() {
            panic!("FloatKey cannot be created with NaN value");
        }
        FloatKey(value)
    }
}

impl Eq for FloatKey {}

impl Ord for FloatKey {
    fn cmp(&self, other: &Self) -> Ordering {
        self.partial_cmp(other)
            .expect("No NaNs allowed, so this will never panic")
    }
}

#[derive(Debug, PartialEq)]
pub(crate) struct SortedMultiMap<K: Ord, V: PartialEq> {
    inner: BTreeMap<K, Vec<V>>,
}

impl<K: Ord, V: PartialEq> SortedMultiMap<K, V> {
    pub fn new() -> Self {
        SortedMultiMap {
            inner: BTreeMap::new(),
        }
    }

    pub fn insert(&mut self, key: K, value: V) {
        self.inner.entry(key).or_insert_with(Vec::new).push(value);
    }

    pub fn delete(&mut self, key: &K, value: &V) -> bool {
        if let Some(values) = self.inner.get_mut(key) {
            if let Some(pos) = values.iter().position(|v| v == value) {
                values.remove(pos);
                if values.is_empty() {
                    self.inner.remove(key);
                }
                return true;
            }
        }
        false
    }

    pub fn iter(&self) -> impl Iterator<Item = (&K, &V)> {
        self.inner
            .iter()
            .flat_map(|(key, values)| values.iter().map(move |value| (key, value)))
    }

    pub fn is_empty(&self) -> bool {
        self.inner.is_empty()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sorted_multi_map_insert() {
        let mut map = SortedMultiMap::new();
        map.insert(FloatKey::new(1.0), 1);
        map.insert(FloatKey::new(1.0), 2);
        map.insert(FloatKey::new(2.0), 3);

        let mut iter = map.iter();

        assert_eq!(iter.next(), Some((&FloatKey::new(1.0), &1)));
        assert_eq!(iter.next(), Some((&FloatKey::new(1.0), &2)));
        assert_eq!(iter.next(), Some((&FloatKey::new(2.0), &3)));
        assert_eq!(iter.next(), None);
    }

    #[test]
    fn test_sorted_multi_map_delete() {
        let mut map = SortedMultiMap::new();
        map.insert(FloatKey::new(1.0), 1);
        map.insert(FloatKey::new(1.0), 2);
        map.insert(FloatKey::new(2.0), 3);

        assert!(map.delete(&FloatKey::new(1.0), &1));
        assert!(map.delete(&FloatKey::new(2.0), &3));
        assert!(!map.delete(&FloatKey::new(2.0), &3));

        let mut iter = map.iter();

        assert_eq!(iter.next(), Some((&FloatKey::new(1.0), &2)));
        assert_eq!(iter.next(), None);
    }

    #[test]
    fn test_sorted_multi_map_is_empty() {
        let mut map = SortedMultiMap::new();

        map.insert(FloatKey::new(1.0), 1);
        assert_eq!(map.is_empty(), false);

        map.delete(&FloatKey::new(1.0), &1);
        assert!(map.is_empty());
    }
}
