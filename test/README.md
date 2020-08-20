## Preflight Test

This test should be run before submitting your challenge.

The test will check:
 - All the links are correct and working.
 - All the ids needed for a further automatic test are present and in their place.

# How to run:

1. Install dependencies
```
  npm install
```

2. Run test
```
  npm test pre_test.js
```

**Note**: The test is configure to run locally. In case your challenge run in a different port that 4242, modify [pre_test.js](/pre_test.js).

```javascript
const url = 'http://localhost:port';
```

**Note**: If you are using react client, change the port for 3000 or the port where react is running.
