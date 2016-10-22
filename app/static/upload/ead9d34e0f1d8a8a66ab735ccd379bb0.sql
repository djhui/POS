-- --------------------------------------------------------
-- 主机:                           172.18.1.254
-- 服务器版本:                        5.1.73 - Source distribution
-- 服务器操作系统:                      openwrt-linux-gnu
-- HeidiSQL 版本:                  9.1.0.4867
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
-- 正在导出表  wechat_command.do 的数据：18 rows
/*!40000 ALTER TABLE `do` DISABLE KEYS */;
INSERT INTO `do` (`id`, `message`, `commands`, `user_level`) VALUES
	(2, '开关热水器', 'python /root/plugins/water_heater.py', NULL),
	(1, '强制开关热水器', 'python /root/plugins/water_heater.py force', NULL),
	(3, '预约热水器', 'python /root/plugins/water_heater_Book.py book', NULL),
	(4, '取消热水器', 'python /root/plugins/water_heater_Book.py cancel', NULL),
	(5, '禁用热水器', 'python /root/plugins/water_heater_Book.py disable', NULL),
	(6, '重启副路由', 'python /root/plugins/router.py', NULL),
	(7, '打开电脑', '/usr/bin/etherwake -D -i "br-lan"  "6c:f0:49:b6:f0:28"', NULL),
	(8, 'IP', 'curl  --interface pppoe-wan "http://www.3322.org/dyndns/getip"', NULL),
	(9, '重启主路由', 'reboot', NULL),
	(10, '家里有人吗', 'fping htc.lan -A', NULL),
	(11, '电视机状态', 'fping hisense.lan ', NULL),
	(12, '帮助', 'python /root/plugins/help_command.py', NULL),
	(13, '遥控', 'http://GoFlex.lan/rc/', NULL),
	(14, '储存状态', 'python /root/plugins/hddtemp.py', NULL),
	(15, '遥控器', 'echo http://172.18.1.245/rc/', NULL),
	(16, '开关电视', NULL, NULL),
	(17, '开关天猫魔盒', NULL, NULL),
	(18, '下载', 'python /root/plugins/download.py', NULL);
/*!40000 ALTER TABLE `do` ENABLE KEYS */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
