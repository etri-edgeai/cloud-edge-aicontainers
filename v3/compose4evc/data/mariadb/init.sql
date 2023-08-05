SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

---------------------------------------------------------
--- db
---------------------------------------------------------
CREATE DATABASE IF NOT EXISTS grafana;
USE grafana;

CREATE TABLE `users` (
  `id` int NOT NULL,
  `username` varchar(30) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `reg_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `users` (`id`, `username`, `email`, `password`, `reg_date`) VALUES
(10, 'jpark', 'jpark@keti.re.kr', '$2y$10$OAHnQ1/9POEOJgfWANxyE.muavtXJOZVphdcpn5Ai1sijuGtm17N2', '2023-08-03 02:15:36'),
(11, 'test', 'test@test.net', '$2y$10$24f5p4slS/2UaCATIbKAoup3zqPmzjz7JNMDHbWj8tjUJTLXr.RNy', '2023-08-03 07:36:52');

---------------------------------------------------------
--- db
---------------------------------------------------------
CREATE DATABASE IF NOT EXISTS mydb2;
USE mydb2;

CREATE TABLE `users` (
  `id` int NOT NULL,
  `username` varchar(30) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `reg_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


INSERT INTO `users` (`id`, `username`, `email`, `password`, `reg_date`) VALUES
(10, 'jpark', 'jpark@keti.re.kr', '$2y$10$OAHnQ1/9POEOJgfWANxyE.muavtXJOZVphdcpn5Ai1sijuGtm17N2', '2023-08-03 02:15:36'),
(11, 'test', 'test@test.net', '$2y$10$24f5p4slS/2UaCATIbKAoup3zqPmzjz7JNMDHbWj8tjUJTLXr.RNy', '2023-08-03 07:36:52');







---------------------------------------------------------
--- db
---------------------------------------------------------


CREATE DATABASE IF NOT EXISTS evc;
USE evc;

--
-- 데이터베이스: `evc`
--

-- --------------------------------------------------------

--
-- 테이블 구조 `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `username` varchar(30) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `reg_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- 테이블의 덤프 데이터 `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `reg_date`) VALUES
(10, 'jpark', 'jpark@keti.re.kr', '$2y$10$OAHnQ1/9POEOJgfWANxyE.muavtXJOZVphdcpn5Ai1sijuGtm17N2', '2023-08-03 02:15:36'),
(11, 'test', 'test@test.net', '$2y$10$24f5p4slS/2UaCATIbKAoup3zqPmzjz7JNMDHbWj8tjUJTLXr.RNy', '2023-08-03 07:36:52');
--
-- 덤프된 테이블의 인덱스
--

--
-- 테이블의 인덱스 `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- 덤프된 테이블의 AUTO_INCREMENT
--

--
-- 테이블의 AUTO_INCREMENT `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
