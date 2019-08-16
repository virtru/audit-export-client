# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased](https://github.com/virtru/virtru-audit-export-client/compare/master...HEAD)

## [2.0.3](https://github.com/virtru/audit-export-client/pull/10) - 2019-08-16
## Fixed
  - Fix export to csv so that exported file does not duplicate csv headers
  - Rewrite csv file to path specified at runtime instead of appending

## [2.0.2](https://github.com/virtru/audit-export-client/pull/9) - 2019-05-07
## Added
  - Add leeway to `iat` field of token to account for clock skew
  - Add  `MIT` license

## [2.0.1](https://github.com/virtru/audit-export-client/pull/7) - 2019-04-24
## Fixed
  - Address vulnerability with `urllib3`

## [2.0.0](https://github.com/virtru/audit-export-client/pull/5) - 2019-03-25
## Added
 - Changed cli logic for using elastic search api
 - Using cursor logic instead bookmark

## [1.1.0](https://github.com/virtru/audit-export-client/pull/4) - 2018-10-31
## Added
 - Added tests
 - Fixed re-initialization of syslog handler
 - added `-v` flag for verbose logs
 - Refactored code to be more pythonic :snake:

## [1.0.0] - 2018-09-06
### Added
 - Init project
