USE [master]
GO
/****** Object:  Database [Stock]    Script Date: 2021-09-28 오후 9:03:12 ******/
CREATE DATABASE [Stock]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'Stock', FILENAME = N'D:\Program Files\Microsoft SQL Server\MSSQL15.MSSQLSERVER\MSSQL\DATA\Stock.mdf' , SIZE = 663552KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'Stock_log', FILENAME = N'D:\Program Files\Microsoft SQL Server\MSSQL15.MSSQLSERVER\MSSQL\DATA\Stock_log.ldf' , SIZE = 401408KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT
GO
ALTER DATABASE [Stock] ADD FILEGROUP [1]
GO
ALTER DATABASE [Stock] ADD FILEGROUP [10]
GO
ALTER DATABASE [Stock] ADD FILEGROUP [11]
GO
ALTER DATABASE [Stock] ADD FILEGROUP [12]
GO
ALTER DATABASE [Stock] ADD FILEGROUP [2]
GO
ALTER DATABASE [Stock] ADD FILEGROUP [3]
GO
ALTER DATABASE [Stock] ADD FILEGROUP [4]
GO
ALTER DATABASE [Stock] ADD FILEGROUP [5]
GO
ALTER DATABASE [Stock] ADD FILEGROUP [6]
GO
ALTER DATABASE [Stock] ADD FILEGROUP [7]
GO
ALTER DATABASE [Stock] ADD FILEGROUP [8]
GO
ALTER DATABASE [Stock] ADD FILEGROUP [9]
GO
ALTER DATABASE [Stock] SET COMPATIBILITY_LEVEL = 150
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [Stock].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [Stock] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [Stock] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [Stock] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [Stock] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [Stock] SET ARITHABORT OFF 
GO
ALTER DATABASE [Stock] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [Stock] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [Stock] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [Stock] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [Stock] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [Stock] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [Stock] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [Stock] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [Stock] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [Stock] SET  DISABLE_BROKER 
GO
ALTER DATABASE [Stock] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [Stock] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [Stock] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [Stock] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [Stock] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [Stock] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [Stock] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [Stock] SET RECOVERY FULL 
GO
ALTER DATABASE [Stock] SET  MULTI_USER 
GO
ALTER DATABASE [Stock] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [Stock] SET DB_CHAINING OFF 
GO
ALTER DATABASE [Stock] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [Stock] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [Stock] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [Stock] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
ALTER DATABASE [Stock] SET QUERY_STORE = OFF
GO
USE [Stock]
GO
/****** Object:  Table [dbo].[AllTimePriceFromNaver]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[AllTimePriceFromNaver](
	[AllTimePriceId] [int] IDENTITY(1,1) NOT NULL,
	[code] [nvarchar](100) NULL,
	[startval] [real] NULL,
	[highval] [real] NULL,
	[lowval] [real] NULL,
	[curval] [real] NULL,
	[curvol] [real] NULL,
	[Regdate] [datetime] NULL,
 CONSTRAINT [PK_AllTimePriceFromNaver] PRIMARY KEY CLUSTERED 
(
	[AllTimePriceId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[AllTimePriceFromNaver_20201207]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[AllTimePriceFromNaver_20201207](
	[AllTimePriceId] [int] IDENTITY(1,1) NOT NULL,
	[code] [nvarchar](100) NULL,
	[startval] [real] NULL,
	[highval] [real] NULL,
	[lowval] [real] NULL,
	[curval] [real] NULL,
	[curvol] [real] NULL,
	[Regdate] [datetime] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Category]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Category](
	[CategoryId] [int] IDENTITY(1,1) NOT NULL,
	[category] [nvarchar](100) NULL,
	[categoryname] [nvarchar](100) NOT NULL,
	[Regdate] [datetime] NOT NULL,
 CONSTRAINT [PK_Upjong] PRIMARY KEY CLUSTERED 
(
	[CategoryId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[CategoryDetail]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[CategoryDetail](
	[CategoryDetailId] [int] IDENTITY(1,1) NOT NULL,
	[CategoryId] [int] NOT NULL,
	[name] [nvarchar](100) NOT NULL,
	[Regdate] [datetime] NOT NULL,
 CONSTRAINT [PK_UpjongDetail] PRIMARY KEY CLUSTERED 
(
	[CategoryDetailId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Code]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Code](
	[code] [nvarchar](50) NOT NULL,
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[name] [nvarchar](100) NULL,
	[category] [nvarchar](200) NULL,
	[products] [nvarchar](800) NULL,
	[issuedate] [datetime] NULL,
	[settlementdate] [nvarchar](30) NULL,
 CONSTRAINT [PK_Code] PRIMARY KEY CLUSTERED 
(
	[code] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[DailyEtfPrice]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[DailyEtfPrice](
	[EtfPriceId] [int] IDENTITY(1,1) NOT NULL,
	[code] [varchar](50) NULL,
	[date] [date] NULL,
	[closeprice] [bigint] NULL,
	[pricediff] [bigint] NULL,
	[openprice] [float] NULL,
	[highprice] [float] NULL,
	[lowprice] [float] NULL,
	[volume] [bigint] NULL,
	[yeardate] [bigint] NULL,
	[monthdate] [bigint] NULL,
 CONSTRAINT [PK_DailyEtfPrice] PRIMARY KEY CLUSTERED 
(
	[EtfPriceId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[DailyPrice]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[DailyPrice](
	[PriceId] [int] IDENTITY(1,1) NOT NULL,
	[code] [nvarchar](50) NULL,
	[date] [date] NULL,
	[closeprice] [float] NULL,
	[pricediff] [float] NULL,
	[openprice] [float] NULL,
	[highprice] [float] NULL,
	[lowprice] [float] NULL,
	[volume] [float] NULL,
	[yeardate] [int] NULL,
	[monthdate] [int] NULL,
 CONSTRAINT [PK_DailyPrice] PRIMARY KEY CLUSTERED 
(
	[PriceId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[ErrorLog]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ErrorLog](
	[ErrorLogId] [int] IDENTITY(1,1) NOT NULL,
	[Origin] [nvarchar](100) NOT NULL,
	[Comment] [nvarchar](max) NOT NULL,
	[Regdate] [datetime] NOT NULL,
 CONSTRAINT [PK_ErrorLog] PRIMARY KEY CLUSTERED 
(
	[ErrorLogId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[EtfCode]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[EtfCode](
	[ShortCode] [varchar](50) NOT NULL,
	[StandardCode] [varchar](max) NULL,
	[KoreanName] [varchar](max) NULL,
	[KoreanShortName] [varchar](max) NULL,
	[EnglishName] [varchar](max) NULL,
	[ListedDate] [varchar](max) NULL,
	[BasicIndexName] [varchar](max) NULL,
	[IndexCompany] [varchar](max) NULL,
	[TrackingMultiple] [varchar](max) NULL,
	[ReplicationMethod] [varchar](max) NULL,
	[BasicMarketClassification] [varchar](max) NULL,
	[BasicAssetClassification] [varchar](max) NULL,
	[ListedNumber] [bigint] NULL,
	[Operator] [varchar](max) NULL,
	[CUQuantity] [bigint] NULL,
	[GrossRemuneration] [float] NULL,
	[Tax Type] [varchar](max) NULL,
 CONSTRAINT [PK_EtfCode] PRIMARY KEY CLUSTERED 
(
	[ShortCode] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Issue]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Issue](
	[IssueId] [int] IDENTITY(1,1) NOT NULL,
	[code] [nvarchar](50) NOT NULL,
	[comment] [nvarchar](max) NOT NULL,
	[sentviakakao] [bit] NOT NULL,
	[Regdate] [datetime] NOT NULL,
 CONSTRAINT [PK_Issue] PRIMARY KEY CLUSTERED 
(
	[IssueId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Jackpot]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Jackpot](
	[JackpotId] [int] IDENTITY(1,1) NOT NULL,
	[Regdate] [datetime] NULL,
	[cate] [nvarchar](100) NULL,
	[code] [nvarchar](100) NULL,
	[name] [nvarchar](100) NULL,
	[startval] [float] NULL,
	[startvol] [float] NULL,
	[curval] [float] NULL,
	[curvol] [float] NULL,
	[startvol_curvol_diff] [float] NULL,
	[startval_curval_diff] [float] NULL,
	[avg3] [float] NULL,
	[avg7] [float] NULL,
	[val_infle] [bigint] NULL,
	[vol_infle] [bigint] NULL,
	[curval_1diff] [float] NULL,
	[curvol_1diff] [float] NULL,
	[avg3_1diff] [float] NULL,
	[avg7_1diff] [float] NULL,
	[curval_3diff] [float] NULL,
	[curvol_3diff] [float] NULL,
	[avg3_3diff] [float] NULL,
	[avg7_3diff] [float] NULL,
	[high] [float] NULL,
	[low] [float] NULL,
	[revert_trend] [bit] NULL,
	[timehour]  AS (datepart(hour,[Regdate])),
 CONSTRAINT [PK_Jackpot] PRIMARY KEY CLUSTERED 
(
	[JackpotId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[KakaoAuthInfo]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[KakaoAuthInfo](
	[code] [nvarchar](500) NULL,
	[access_token] [nvarchar](500) NULL,
	[refresh_token] [nvarchar](500) NULL,
	[expires_in] [int] NOT NULL,
	[scope] [nvarchar](100) NULL,
	[refresh_token_expires_in] [int] NULL,
	[Regdate] [datetime] NULL,
 CONSTRAINT [PK_KakaoAuthInfo] PRIMARY KEY CLUSTERED 
(
	[expires_in] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[KakaoRecipients]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[KakaoRecipients](
	[KakaoRecipientsId] [int] IDENTITY(1,1) NOT NULL,
	[name] [nvarchar](50) NOT NULL,
	[emailaddr] [nvarchar](100) NOT NULL,
	[Regdate] [datetime] NOT NULL,
 CONSTRAINT [PK_KakaoRecipients] PRIMARY KEY CLUSTERED 
(
	[KakaoRecipientsId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[KakaoRefInfo]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[KakaoRefInfo](
	[REST_API_KEY] [nvarchar](100) NOT NULL,
	[REDIRECT_URI] [nvarchar](100) NULL,
	[AUTH_URL] [nvarchar](100) NULL,
	[TOKEN_URL] [nvarchar](100) NULL,
 CONSTRAINT [PK_KakaoRefInfo] PRIMARY KEY CLUSTERED 
(
	[REST_API_KEY] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[KakaoRestService]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[KakaoRestService](
	[KakaoRestServiceId] [int] IDENTITY(1,1) NOT NULL,
	[RestServiceName] [nvarchar](100) NULL,
	[RestServiceUrl] [nvarchar](300) NULL,
	[Regdate] [datetime] NULL,
 CONSTRAINT [PK_KakaoRestService] PRIMARY KEY CLUSTERED 
(
	[KakaoRestServiceId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[KeyItem]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[KeyItem](
	[KeyItemId] [int] IDENTITY(1,1) NOT NULL,
	[issuedate] [date] NULL,
	[category] [nvarchar](50) NULL,
	[code] [nvarchar](50) NULL,
	[Regdate] [datetime] NULL,
 CONSTRAINT [PK_KeyItem] PRIMARY KEY CLUSTERED 
(
	[KeyItemId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Number]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Number](
	[Days] [int] NOT NULL,
 CONSTRAINT [PK_Number] PRIMARY KEY CLUSTERED 
(
	[Days] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[PriceAfterWorkingHour]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[PriceAfterWorkingHour](
	[PriceAfterHourId] [int] IDENTITY(1,1) NOT NULL,
	[rank] [bigint] NULL,
	[code] [nvarchar](50) NULL,
	[name] [nvarchar](100) NULL,
	[symbolCode] [nvarchar](100) NULL,
	[fullcode] [nvarchar](100) NULL,
	[tradePrice] [float] NULL,
	[change] [nvarchar](100) NULL,
	[changePrice] [float] NULL,
	[changeRate] [float] NULL,
	[pricePerformance] [float] NULL,
	[accTradeVolume] [bigint] NULL,
	[accTradePrice] [bigint] NULL,
	[regularHoursTradePrice] [float] NULL,
	[regularHoursChange] [nvarchar](100) NULL,
	[regularHoursChangePrice] [float] NULL,
	[regularHoursChangeRate] [float] NULL,
	[date] [date] NULL,
	[cate] [nvarchar](150) NULL,
	[Regdate] [datetime] NULL,
 CONSTRAINT [PK_PriceAfterWorkingHour] PRIMARY KEY CLUSTERED 
(
	[PriceAfterHourId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[StockService]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[StockService](
	[StockServiceId] [int] IDENTITY(1,1) NOT NULL,
	[ServiceName] [nvarchar](100) NOT NULL,
	[IntervalSeconds] [int] NOT NULL,
	[ServiceStartHour] [int] NOT NULL,
	[ServiceStartMin] [int] NOT NULL,
	[ServiceEndHour] [int] NOT NULL,
	[ServiceEndMin] [int] NOT NULL,
	[Regdate] [datetime] NOT NULL,
 CONSTRAINT [PK_StockService] PRIMARY KEY CLUSTERED 
(
	[StockServiceId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Theme]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Theme](
	[ThemeId] [int] IDENTITY(1,1) NOT NULL,
	[themename] [nvarchar](100) NULL,
	[Regdate] [datetime] NULL,
 CONSTRAINT [PK_Theme] PRIMARY KEY CLUSTERED 
(
	[ThemeId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [idx_code]    Script Date: 2021-09-28 오후 9:03:12 ******/
CREATE NONCLUSTERED INDEX [idx_code] ON [dbo].[AllTimePriceFromNaver]
(
	[code] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [idx_date]    Script Date: 2021-09-28 오후 9:03:12 ******/
CREATE NONCLUSTERED INDEX [idx_date] ON [dbo].[AllTimePriceFromNaver]
(
	[Regdate] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [<Name of Missing Index, sysname,>]    Script Date: 2021-09-28 오후 9:03:12 ******/
CREATE NONCLUSTERED INDEX [<Name of Missing Index, sysname,>] ON [dbo].[DailyPrice]
(
	[date] ASC
)
INCLUDE([code],[closeprice]) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [idx_code]    Script Date: 2021-09-28 오후 9:03:12 ******/
CREATE NONCLUSTERED INDEX [idx_code] ON [dbo].[DailyPrice]
(
	[code] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [idx_date]    Script Date: 2021-09-28 오후 9:03:12 ******/
CREATE NONCLUSTERED INDEX [idx_date] ON [dbo].[DailyPrice]
(
	[date] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [idx_search]    Script Date: 2021-09-28 오후 9:03:12 ******/
CREATE NONCLUSTERED INDEX [idx_search] ON [dbo].[Jackpot]
(
	[Regdate] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
ALTER TABLE [dbo].[Category] ADD  CONSTRAINT [DF_Upjong_Regdate]  DEFAULT (getdate()) FOR [Regdate]
GO
ALTER TABLE [dbo].[CategoryDetail] ADD  CONSTRAINT [DF_UpjongDetail_Regdate]  DEFAULT (getdate()) FOR [Regdate]
GO
ALTER TABLE [dbo].[ErrorLog] ADD  CONSTRAINT [DF_ErrorLog_Regdate]  DEFAULT (getdate()) FOR [Regdate]
GO
ALTER TABLE [dbo].[Issue] ADD  CONSTRAINT [DF_Issue_sentviakakao]  DEFAULT ((0)) FOR [sentviakakao]
GO
ALTER TABLE [dbo].[Issue] ADD  CONSTRAINT [DF_Issue_Regdate]  DEFAULT (getdate()) FOR [Regdate]
GO
ALTER TABLE [dbo].[KakaoAuthInfo] ADD  CONSTRAINT [DF_KakaoAuthInfo_Regdate]  DEFAULT (getdate()) FOR [Regdate]
GO
ALTER TABLE [dbo].[KakaoRecipients] ADD  CONSTRAINT [DF_KakaoRecipients_Regdate]  DEFAULT (getdate()) FOR [Regdate]
GO
ALTER TABLE [dbo].[KakaoRestService] ADD  CONSTRAINT [DF_KakaoRestService_Regdate]  DEFAULT (getdate()) FOR [Regdate]
GO
ALTER TABLE [dbo].[KeyItem] ADD  CONSTRAINT [DF_KeyItem_Regdate]  DEFAULT (getdate()) FOR [Regdate]
GO
ALTER TABLE [dbo].[PriceAfterWorkingHour] ADD  CONSTRAINT [DF_PriceAfterWorkingHour_Regdate]  DEFAULT (getdate()) FOR [Regdate]
GO
ALTER TABLE [dbo].[StockService] ADD  CONSTRAINT [DF_StockService_Regdate]  DEFAULT (getdate()) FOR [Regdate]
GO
ALTER TABLE [dbo].[Theme] ADD  CONSTRAINT [DF_Theme_Regdate]  DEFAULT (getdate()) FOR [Regdate]
GO
ALTER TABLE [dbo].[CategoryDetail]  WITH CHECK ADD  CONSTRAINT [FK_CategoryDetail_Category] FOREIGN KEY([CategoryId])
REFERENCES [dbo].[Category] ([CategoryId])
GO
ALTER TABLE [dbo].[CategoryDetail] CHECK CONSTRAINT [FK_CategoryDetail_Category]
GO
ALTER TABLE [dbo].[DailyEtfPrice]  WITH CHECK ADD  CONSTRAINT [FK_DailyEtfPrice_EtfCode] FOREIGN KEY([code])
REFERENCES [dbo].[EtfCode] ([ShortCode])
GO
ALTER TABLE [dbo].[DailyEtfPrice] CHECK CONSTRAINT [FK_DailyEtfPrice_EtfCode]
GO
ALTER TABLE [dbo].[DailyPrice]  WITH CHECK ADD  CONSTRAINT [FK_DailyPrice_Code] FOREIGN KEY([code])
REFERENCES [dbo].[Code] ([code])
GO
ALTER TABLE [dbo].[DailyPrice] CHECK CONSTRAINT [FK_DailyPrice_Code]
GO
ALTER TABLE [dbo].[KeyItem]  WITH CHECK ADD  CONSTRAINT [FK_KeyItem_Code] FOREIGN KEY([code])
REFERENCES [dbo].[Code] ([code])
GO
ALTER TABLE [dbo].[KeyItem] CHECK CONSTRAINT [FK_KeyItem_Code]
GO
/****** Object:  StoredProcedure [dbo].[getCategoryPrice]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[getCategoryPrice]
	@fromdate datetime,
	@todate datetime,
	@category nvarchar(50),
	@categoryname nvarchar(100)


AS
BEGIN

--declare @fromdate datetime = '2020-11-01';
--declare @todate  datetime = '2020-11-30';
--declare @category varchar(50) ='업종별';
with
raw
as
(
	select cg.category
		,cg.categoryname
		,c.code
		,c.name
		,dp.date
		,first_value(dp.closeprice) over (partition by cg.categoryname,c.code order by date asc) initprice
		,dp.closeprice
		,COALESCE(lead([closeprice]) over (partition by c.code,cg.categoryname order by date desc),0) prev_price
		,coalesce(round((closeprice - lead([closeprice]) over (partition by c.code,cg.categoryname order by date desc))/(lead([closeprice]) over (order by date desc)) * 100,1),0) diff_rate
	from Category cg
	join CategoryDetail cd
		on cg.CategoryId = cd.CategoryId
	join Code c
		on cd.name = c.name	
	join DailyPrice dp
		on dp.code = c.code
	where dp.date between @fromdate and @todate 	
		and 1 = (case when @category is null then 1 when cg.category=@category then 1 else 0 end)
		and 1 = (case when @categoryname is null then 1 when cg.categoryname = @categoryname then 1 else 0 end)
)
select *,
	round(avg(diff_rate) over (partition by category,categoryname,date),1) diff_rate_avg
	from raw
	order by code,categoryname,date
END
GO
/****** Object:  StoredProcedure [dbo].[getChartData]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[getChartData]
	@min int,
	@code nvarchar(50)
AS
BEGIN
	
	SELECT [AllTimePriceId]
      ,[code]
      ,[startval]
      ,[highval]
      ,[lowval]
      ,[curval]
      ,[curvol] as cumvol      
	  ,[curvol] - lead(curvol) over (partition by code order by Regdate desc) as curvol
	  ,Regdate
	from AllTimePriceFromNaver
	where Regdate >= dateadd(minute,-1*@min,getdate()) and code=@code
	order by Regdate
END
GO
/****** Object:  StoredProcedure [dbo].[getCurrentTrendValue]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[getCurrentTrendValue]	
	@code nvarchar(50),
	@durationhour int	
AS
BEGIN
	select code
		,Regdate
		,curval
		,curvol
		,round(((curval-befval)/befval) * 100,1) diffval
		,round(((curval-highval)/highval) * 100,1) diffhighval
		,round(((curval-lowval)/lowval) * 100,1) difflowval
		,round(((curvol-befvol)/befvol) * 100,1) diffvol
	from 
	(
	select code
		,startval
		,highval
		,lowval
		,curval
		,COALESCE(lag(curval) over (partition by code order by Regdate),curval) befval
		,curvol
		,COALESCE(lag(curvol) over (partition by code order by Regdate),curvol) befvol
		,Regdate
	from AllTimePriceFromNaver
	where code = @code
		and Regdate >= dateadd(hour,-1 * @durationhour,getdate())
	) s
	order by Regdate
END
GO
/****** Object:  StoredProcedure [dbo].[getGroupbyCategory]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[getGroupbyCategory]
	-- Add the parameters for the stored procedure here
	@duration int = 60 
AS
BEGIN
	with joined
as
(
select  c.category
		,c.categoryname
		,cd.name
		,code.code
		,code.category as codecategory
		,d.date
		,case when (d.closeprice - d.pricediff) <> 0 then pricediff / cast(d.closeprice - d.pricediff as real) else 0 end as diffratio
from Category c
join CategoryDetail cd
	on c.CategoryId = cd.CategoryId
join Code code
	on cd.name = code.name
join DailyPrice d
	on d.code = code.code
where d.date between dateadd(d,-1* @duration,getdate()) and getdate()
)
select category,categoryname,date,round(avg(diffratio)*100,2) as avgdiff
from joined
group by category,categoryname,date
order by category,categoryname,date desc
END
GO
/****** Object:  StoredProcedure [dbo].[getIssue]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
CREATE PROCEDURE [dbo].[getIssue]
	@min int
AS
BEGIN
	
	select c.name, i.*,
	'https://m.stock.naver.com/item/main.nhn#/stocks/' + i.code + '/total' as Url
	from Issue i
	join code c
		on i.code =c.code
	
	where Regdate >= dateadd(minute,-1*@min,getdate())
	order by Regdate desc
END
GO
/****** Object:  StoredProcedure [dbo].[getJackPotStatus]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[getJackPotStatus]
	@min int
AS
BEGIN
	with base
	as
	(
		select *
		from Jackpot
		where Regdate >= dateadd(minute,-1 * @min,getdate())
	),
	isscnt
	as
	(
		select code,count(1) cnt
		from base
		group by code
	),
	theme
	as
	(
		SELECT
		 cc.code
		  ,cc.[name]
	
		  ,string_agg(c.categoryname,',') as catelist
  
	  FROM [Stock].[dbo].[CategoryDetail] cd
	  join Category c
		on cd.CategoryId = c.CategoryId
	  join Code cc
		on cd.name = cc.name
  
	  group by cc.code,cc.name

	),
	ccc
	as
	(
	select *
	from code
	)
	select c.cnt, [Regdate]
      ,[cate]
      ,b.[code]
      ,b.[name]
	  ,code.category
	  ,code.products
	  ,c.cnt 
	  ,t.catelist
      ,[startval]
      ,[startvol]
      ,[curval]
      ,[curvol]
      ,[startvol_curvol_diff]
      ,[startval_curval_diff]
      ,[avg3]
      ,[avg7]
      ,[val_infle]
      ,[vol_infle]
      ,[curval_1diff]
      ,[curvol_1diff]
      ,[avg3_1diff]
      ,[avg7_1diff]
      ,[curval_3diff]
      ,[curvol_3diff]
      ,[avg3_3diff]
      ,[avg7_3diff]
      ,[high]
      ,[low]
      ,case when [revert_trend] is null then 0 else revert_trend end revert_trend
	from base b
	join isscnt c
		 on b.code = c.code
	left join theme t
		on b.code = t.code
	left join ccc code
		on b.code = code.code
	order by Regdate desc, c.cnt desc
END
GO
/****** Object:  StoredProcedure [dbo].[getKeyItemList]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
CREATE PROCEDURE [dbo].[getKeyItemList]	
	-- Add the parameters for the stored procedure here
	@from datetime,
	@to datetime
AS
BEGIN
with
lastdate
as
(
	select max(date) date
	from DailyPrice
),
lastvalue
as
(
	select d.*
	from DailyPrice d
	join lastdate l
		on d.date = l.date
	where  code in (select code
	from KeyItem k
	where k.issuedate between @from and @to)

)	
select distinct
    p.cate as KospiKosdaq
	,k.code as Code
	,k.issuedate as Date
	,k.category as Cate
	,c.name as Name
	,p.fullcode as DaumCode
	,'https://m.stock.naver.com/item/main.nhn#/stocks/' + k.code + '/total' as Url
	,case when p.[rank] is null then '-1' else p.[rank] end as [rank]
	,p.tradePrice as TradePrice
	,d.closeprice as ClosePrice
	,lv.closeprice as lastdayClosePrice
	,d.volume as TradeVolume
	,p.regularHoursChangePrice as RegularHoursChangePrice
	,p.regularHoursChangeRate as RegularHoursChnageRate
	,p.changeRate as ChangeRate
from KeyItem k
join Code c
	on k.code = c.code
join DailyPrice d
	on k.code = d.code
		and k.issuedate = d.[date]
join lastvalue lv
	on k.code =lv.code
left join PriceAfterWorkingHour p
	on k.code = p.code
	and k.issuedate = p.date
where k.issuedate between @from and @to



END
GO
/****** Object:  StoredProcedure [dbo].[getPivotedJackPotData]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[getPivotedJackPotData]
	@min int
AS
BEGIN
	select *
	from 
	(
	SELECT name,code,cast(Regdate as date) date, count(1) cnt
	from Jackpot
	where Regdate >= DATEADD(MINUTE,-1 * @min,getdate())
	group by code,name,cast(Regdate as date)
	) s
	order by date desc, s.cnt desc
END
GO
/****** Object:  StoredProcedure [dbo].[getThemeForName]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
CREATE PROCEDURE [dbo].[getThemeForName]
	@name nvarchar
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	SELECT
		 cc.code
		  ,cc.[name]
	
		  ,string_agg(c.categoryname,',') as catelist
  
	  FROM [Stock].[dbo].[CategoryDetail] cd
	  join Category c
		on cd.CategoryId = c.CategoryId
	  join Code cc
		on cd.name = cc.name
	  where cc.name = @name
  
	  group by cc.code,cc.name
END
GO
/****** Object:  StoredProcedure [dbo].[PriceChangeStatus]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
CREATE PROCEDURE [dbo].[PriceChangeStatus]
	@issuedate datetime
	,@duration int = 7
AS
BEGIN
	select i.category
	,i.code	
	,c.name
	,c.category
	,i.issuedate
	,pp.closeprice issuedateprice
	,p.date 
	,p.closeprice
	,p.closeprice - pp.closeprice closepricediff
	,round(cast((p.closeprice - pp.closeprice) as float)/cast(pp.closeprice as float) * 100,1) closepricediffratio
	,p.highprice
	,p.highprice - pp.closeprice highpricediff
	,round(cast((p.highprice - pp.closeprice) as float)/cast(pp.closeprice as float) * 100,1) highpricediffratio
	,p.lowprice
	,p.lowprice - pp.closeprice lowpricediff
	,round(cast((p.lowprice - pp.closeprice) as float)/cast(pp.closeprice as float) * 100,1) lowpricediffratio	
	,p.pricediff
	from KeyItem i
	join DailyPrice p
		on i.code = p.code
		and p.date > i.issuedate and p.date <= dateadd(d,@duration,i.issuedate)
	join (select code, closeprice from DailyPrice where date = @issuedate) pp
		on i.code = pp.code
	join Code c
		on i.code = c.code
	where i.issuedate = @issuedate
	order by i.category,code,date

END
GO
/****** Object:  StoredProcedure [dbo].[temp]    Script Date: 2021-09-28 오후 9:03:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

create procedure [dbo].[temp]
as

declare @from datetime = '2020-11-27', @to datetime = '2020-11-30';
with
data
as
(
select distinct
    p.cate as KospiKosdaq
	,k.code as Code
	,k.issuedate as Date
	,datediff(day,k.issuedate,getdate()) pastdays
	
	,k.category as Cate
	,c.name as Name
	,p.fullcode as DaumCode
	,'https://m.stock.naver.com/item/main.nhn#/stocks/' + k.code + '/total' as Url
	,case when p.[rank] is null then '-1' else p.[rank] end as [rank]
	,p.tradePrice as TradePrice
	,d.closeprice as ClosePrice
	,d.volume as TradeVolume
	,p.regularHoursChangePrice as RegularHoursChangePrice
	,p.regularHoursChangeRate as RegularHoursChnageRate
	,p.changeRate as ChangeRate
from KeyItem k
join Code c
	on k.code = c.code
join DailyPrice d
	on k.code = d.code
		and k.issuedate = d.[date]
left join PriceAfterWorkingHour p
	on k.code = p.code
	and k.issuedate = p.date
where k.issuedate between @from and @to
)
select *
from data
where pastdays <=7
GO
USE [master]
GO
ALTER DATABASE [Stock] SET  READ_WRITE 
GO
