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
        self.partial_cmp(other).expect("No NaNs allowed, so this will never panic")
    }
}

#[derive(Debug)]
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
}