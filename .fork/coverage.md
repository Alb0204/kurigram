# Fork coverage

| Number | Now | Baseline |
|--------|-----|----------|
| `layers_behind` | 0 | 0 |
| `raw_unwrapped` | 489 | 490 |
| `bot_api_gaps` | 141 | 141 |

## Layer drift

Our schema: layer 232. tdesktop `dev`: layer 232.

Every combinator matches.

## Raw API coverage

330 of 819 tracked raw functions are called by a high-level method; 489 are not. `coverage_ignore.toml` leaves out the ones that should never get a wrapper.

| Namespace | Unwrapped | Tracked |
|-----------|-----------|---------|
| messages | 140 | 261 |
| account | 96 | 128 |
| phone | 42 | 43 |
| payments | 40 | 76 |
| bots | 24 | 40 |
| channels | 24 | 58 |
| wallet | 23 | 26 |
| contacts | 18 | 30 |
| stories | 17 | 33 |
| help | 11 | 14 |
| auth | 10 | 25 |
| communities | 9 | 9 |
| stats | 8 | 8 |
| aicompose | 7 | 7 |
| ephemeral | 5 | 8 |
| chatlists | 4 | 11 |
| users | 3 | 7 |
| premium | 2 | 5 |
| toncenter | 2 | 2 |
| fragment | 1 | 1 |
| photos | 1 | 5 |
| stickers | 1 | 11 |
| upload | 1 | 7 |
| folders | 0 | 1 |
| updates | 0 | 3 |

<details><summary>account (96)</summary>

- `account.acceptAuthorization`
- `account.cancelPasswordEmail`
- `account.changeAuthorizationSettings`
- `account.clearRecentEmojiStatuses`
- `account.confirmBotConnection`
- `account.confirmPasswordEmail`
- `account.confirmPhone`
- `account.createBusinessChatLink`
- `account.createTheme`
- `account.declinePasswordReset`
- `account.deleteAccount`
- `account.deleteAutoSaveExceptions`
- `account.deleteBusinessChatLink`
- `account.deletePasskey`
- `account.deleteSecureValue`
- `account.deleteWebBrowserSettingsExceptions`
- `account.disablePeerConnectedBot`
- `account.editBusinessChatLink`
- `account.getAllSecureValues`
- `account.getAuthorizationForm`
- `account.getAutoDownloadSettings`
- `account.getAutoSaveSettings`
- `account.getBusinessChatLinks`
- `account.getChannelDefaultEmojiStatuses`
- `account.getChannelRestrictedStatusEmojis`
- `account.getChatThemes`
- `account.getCollectibleEmojiStatuses`
- `account.getConnectedBots`
- `account.getContactSignUpNotification`
- `account.getContentSettings`
- `account.getDefaultBackgroundEmojis`
- `account.getDefaultGroupPhotoEmojis`
- `account.getDefaultProfilePhotoEmojis`
- `account.getMultiWallPapers`
- `account.getNotifyExceptions`
- `account.getNotifySettings`
- `account.getPaidMessagesRevenue`
- `account.getPasskeys`
- `account.getPasswordSettings`
- `account.getReactionsNotifySettings`
- `account.getRecentEmojiStatuses`
- `account.getSavedMusicIds`
- `account.getSavedRingtones`
- `account.getSecureValue`
- `account.getTheme`
- `account.getThemes`
- `account.getUniqueGiftChatThemes`
- `account.getWallPaper`
- `account.getWallPapers`
- `account.getWebAuthorizations`
- `account.getWebBrowserSettings`
- `account.initPasskeyRegistration`
- `account.installTheme`
- `account.installWallPaper`
- `account.invalidateSignInCodes`
- `account.registerDevice`
- `account.registerPasskey`
- `account.reorderUsernames`
- `account.reportPeer`
- `account.reportProfilePhoto`
- `account.resendPasswordEmail`
- `account.resetNotifySettings`
- `account.resetPassword`
- `account.resetWallPapers`
- `account.resetWebAuthorization`
- `account.resetWebAuthorizations`
- `account.resolveBusinessChatLink`
- `account.saveAutoDownloadSettings`
- `account.saveAutoSaveSettings`
- `account.saveRingtone`
- `account.saveSecureValue`
- `account.saveTheme`
- `account.saveWallPaper`
- `account.sendConfirmPhoneCode`
- `account.setContactSignUpNotification`
- `account.setContentSettings`
- `account.setReactionsNotifySettings`
- `account.toggleConnectedBotPaused`
- `account.toggleNoPaidMessagesException`
- `account.toggleSponsoredMessages`
- `account.toggleUsername`
- `account.toggleWebBrowserSettingsException`
- `account.unregisterDevice`
- `account.updateBusinessAwayMessage`
- `account.updateBusinessGreetingMessage`
- `account.updateBusinessIntro`
- `account.updateBusinessLocation`
- `account.updateBusinessWorkHours`
- `account.updateConnectedBot`
- `account.updateDeviceLocked`
- `account.updateTheme`
- `account.updateWebBrowserSettings`
- `account.uploadRingtone`
- `account.uploadTheme`
- `account.uploadWallPaper`
- `account.verifyPhone`

</details>

<details><summary>aicompose (7)</summary>

- `aicompose.createTone`
- `aicompose.deleteTone`
- `aicompose.getTone`
- `aicompose.getToneExample`
- `aicompose.getTones`
- `aicompose.saveTone`
- `aicompose.updateTone`

</details>

<details><summary>auth (10)</summary>

- `auth.acceptLoginToken`
- `auth.cancelCode`
- `auth.cancelWebTokenAuthorization`
- `auth.checkRecoveryPassword`
- `auth.finishPasskeyLogin`
- `auth.firebasePnvSignUp`
- `auth.importWebTokenAuthorization`
- `auth.initPasskeyLogin`
- `auth.reportMissingCode`
- `auth.resetLoginEmail`

</details>

<details><summary>bots (24)</summary>

- `bots.addPreviewMedia`
- `bots.addUsername`
- `bots.allowSendMessage`
- `bots.answerWebhookJSONQuery`
- `bots.canSendMessage`
- `bots.checkDownloadFileParams`
- `bots.deletePreviewMedia`
- `bots.editPreviewMedia`
- `bots.getBotRecommendations`
- `bots.getPopularAppBots`
- `bots.getPreviewInfo`
- `bots.getPreviewMedias`
- `bots.getRequestedWebViewButton`
- `bots.invokeWebViewCustomMethod`
- `bots.removeUsername`
- `bots.reorderPreviewMedias`
- `bots.reorderUsernames`
- `bots.requestWebViewButton`
- `bots.sendCustomRequest`
- `bots.setCustomVerification`
- `bots.toggleUserEmojiStatusPermission`
- `bots.toggleUsername`
- `bots.updateStarRefProgram`
- `bots.updateUserEmojiStatus`

</details>

<details><summary>channels (24)</summary>

- `channels.checkSearchPostsFlood`
- `channels.convertToGigagroup`
- `channels.deactivateAllUsernames`
- `channels.editLocation`
- `channels.exportMessageLink`
- `channels.getInactiveChannels`
- `channels.getLeftChannels`
- `channels.getMessageAuthor`
- `channels.readMessageContents`
- `channels.reorderUsernames`
- `channels.reportAntiSpamFalsePositive`
- `channels.reportSpam`
- `channels.restrictSponsoredMessages`
- `channels.setBoostsToUnblockRestrictions`
- `channels.setEmojiStickers`
- `channels.setStickers`
- `channels.toggleAntiSpam`
- `channels.toggleAutotranslation`
- `channels.toggleJoinRequest`
- `channels.toggleParticipantsHidden`
- `channels.togglePreHistoryHidden`
- `channels.toggleSignatures`
- `channels.toggleUsername`
- `channels.toggleViewForumAsMessages`

</details>

<details><summary>chatlists (4)</summary>

- `chatlists.getChatlistUpdates`
- `chatlists.getLeaveChatlistSuggestions`
- `chatlists.hideChatlistUpdates`
- `chatlists.joinChatlistUpdates`

</details>

<details><summary>communities (9)</summary>

- `communities.create`
- `communities.getJoinedCommunities`
- `communities.getParticipantJoinedChats`
- `communities.getPeerLinkRequests`
- `communities.toggleAllPeerLinkRequestApproval`
- `communities.toggleCommunityCollapsedInDialogs`
- `communities.toggleParticipantBanned`
- `communities.togglePeerLink`
- `communities.togglePeerLinkRequestApproval`

</details>

<details><summary>contacts (18)</summary>

- `contacts.acceptContact`
- `contacts.blockFromReplies`
- `contacts.deleteByPhones`
- `contacts.editCloseFriends`
- `contacts.exportContactToken`
- `contacts.exportNoPaidMessagesToken`
- `contacts.getBirthdays`
- `contacts.getContactIDs`
- `contacts.getLocated`
- `contacts.getSaved`
- `contacts.getSponsoredPeers`
- `contacts.getStatuses`
- `contacts.importContactToken`
- `contacts.importNoPaidMessagesToken`
- `contacts.resetSaved`
- `contacts.resetTopPeerRating`
- `contacts.setBlocked`
- `contacts.toggleTopPeers`

</details>

<details><summary>ephemeral (5)</summary>

- `ephemeral.deleteAllWelcomeMessages`
- `ephemeral.deleteWelcomeMessage`
- `ephemeral.getCallbackAnswer`
- `ephemeral.getWelcomeMessages`
- `ephemeral.reportMessage`

</details>

<details><summary>fragment (1)</summary>

- `fragment.getCollectibleInfo`

</details>

<details><summary>help (11)</summary>

- `help.dismissSuggestion`
- `help.getCdnConfig`
- `help.getCountriesList`
- `help.getDeepLinkInfo`
- `help.getPassportConfig`
- `help.getPeerColors`
- `help.getPeerProfileColors`
- `help.getPremiumPromo`
- `help.getSupport`
- `help.getTermsOfServiceUpdate`
- `help.getTimezonesList`

</details>

<details><summary>messages (140)</summary>

- `messages.acceptEncryption`
- `messages.acceptUrlAuth`
- `messages.checkHistoryImport`
- `messages.checkHistoryImportPeer`
- `messages.checkQuickReplyShortcut`
- `messages.checkUrlAuthMatchCode`
- `messages.clearAllDrafts`
- `messages.clearRecentReactions`
- `messages.clickSponsoredMessage`
- `messages.composeRichMessageWithAI`
- `messages.declineUrlAuth`
- `messages.deleteChat`
- `messages.deleteFactCheck`
- `messages.deletePhoneCallHistory`
- `messages.deleteQuickReplyMessages`
- `messages.deleteQuickReplyShortcut`
- `messages.discardEncryption`
- `messages.editChatAdmin`
- `messages.editFactCheck`
- `messages.editQuickReplyShortcut`
- `messages.getAllDrafts`
- `messages.getAllStickers`
- `messages.getArchivedStickers`
- `messages.getAttachMenuBot`
- `messages.getAttachMenuBots`
- `messages.getAttachedStickers`
- `messages.getAvailableReactions`
- `messages.getBotApp`
- `messages.getDefaultHistoryTTL`
- `messages.getDefaultTagReactions`
- `messages.getDhConfig`
- `messages.getDialogUnreadMarks`
- `messages.getDocumentByHash`
- `messages.getEmojiGameInfo`
- `messages.getEmojiGroups`
- `messages.getEmojiKeywords`
- `messages.getEmojiKeywordsDifference`
- `messages.getEmojiKeywordsLanguages`
- `messages.getEmojiProfilePhotoGroups`
- `messages.getEmojiStatusGroups`
- `messages.getEmojiStickerGroups`
- `messages.getEmojiStickers`
- `messages.getEmojiURL`
- `messages.getExtendedMedia`
- `messages.getFactCheck`
- `messages.getFeaturedEmojiStickers`
- `messages.getFeaturedStickers`
- `messages.getFutureChatCreatorAfterLeave`
- `messages.getMaskStickers`
- `messages.getMessageEditData`
- `messages.getMessageReactionsList`
- `messages.getMessageReadParticipants`
- `messages.getMessagesReactions`
- `messages.getOldFeaturedStickers`
- `messages.getOutboxReadDate`
- `messages.getPaidReactionPrivacy`
- `messages.getPinnedSavedDialogs`
- `messages.getPollResults`
- `messages.getPollVotes`
- `messages.getPreparedInlineMessage`
- `messages.getQuickReplies`
- `messages.getQuickReplyMessages`
- `messages.getRecentLocations`
- `messages.getRecentReactions`
- `messages.getRichMessage`
- `messages.getSavedGifs`
- `messages.getSavedReactionTags`
- `messages.getScheduledMessages`
- `messages.getSearchResultsCalendar`
- `messages.getSearchResultsPositions`
- `messages.getShareThemeBackdrops`
- `messages.getSponsoredMessages`
- `messages.getStickers`
- `messages.getSuggestedDialogFilters`
- `messages.getTopReactions`
- `messages.getUnreadMentions`
- `messages.getUnreadPollVotes`
- `messages.getUnreadReactions`
- `messages.getWebPage`
- `messages.getWebPagePreview`
- `messages.hidePeerSettingsBar`
- `messages.initHistoryImport`
- `messages.migrateChat`
- `messages.prolongWebView`
- `messages.rateTranscribedAudio`
- `messages.readDiscussion`
- `messages.readEncryptedHistory`
- `messages.readFeaturedStickers`
- `messages.readMessageContents`
- `messages.readPollVotes`
- `messages.readSavedHistory`
- `messages.receivedMessages`
- `messages.receivedQueue`
- `messages.reorderPinnedDialogs`
- `messages.reorderPinnedForumTopics`
- `messages.reorderPinnedSavedDialogs`
- `messages.reorderQuickReplies`
- `messages.report`
- `messages.reportEncryptedSpam`
- `messages.reportMessagesDelivery`
- `messages.reportMusicListen`
- `messages.reportReaction`
- `messages.reportReadMetrics`
- `messages.reportSpam`
- `messages.reportSponsoredMessage`
- `messages.requestChatJoinWebView`
- `messages.requestEncryption`
- `messages.requestUrlAuth`
- `messages.saveDraft`
- `messages.savePreparedInlineMessage`
- `messages.searchCustomEmoji`
- `messages.searchEmojiStickerSets`
- `messages.searchSentMedia`
- `messages.sendBotRequestedPeer`
- `messages.sendEncrypted`
- `messages.sendEncryptedFile`
- `messages.sendEncryptedService`
- `messages.sendQuickReplyMessages`
- `messages.sendScheduledMessages`
- `messages.sendWebViewData`
- `messages.setChatAvailableReactions`
- `messages.setChatTheme`
- `messages.setChatWallPaper`
- `messages.setDefaultHistoryTTL`
- `messages.setDefaultReaction`
- `messages.setEncryptedTyping`
- `messages.setShareTheme`
- `messages.startHistoryImport`
- `messages.toggleBotInAttachMenu`
- `messages.toggleDialogPin`
- `messages.togglePaidReactionPrivacy`
- `messages.togglePeerTranslations`
- `messages.toggleSavedDialogPin`
- `messages.toggleStickerSets`
- `messages.transcribeAudio`
- `messages.translateRichMessage`
- `messages.updateSavedReactionTag`
- `messages.uploadEncryptedFile`
- `messages.uploadImportedMedia`
- `messages.viewSponsoredMessage`

</details>

<details><summary>payments (40)</summary>

- `payments.assignAppStoreTransaction`
- `payments.assignPlayMarketTransaction`
- `payments.canPurchaseStore`
- `payments.checkCanSendGift`
- `payments.clearSavedInfo`
- `payments.connectStarRefBot`
- `payments.createOnrampSession`
- `payments.depositStarGift`
- `payments.displayStarGift`
- `payments.editConnectedStarRefBot`
- `payments.getBankCardData`
- `payments.getConnectedStarRefBot`
- `payments.getConnectedStarRefBots`
- `payments.getCurrencyRates`
- `payments.getGiveawayInfo`
- `payments.getOnrampAvailability`
- `payments.getOnrampBaseCurrencies`
- `payments.getOnrampLimits`
- `payments.getOnrampProviders`
- `payments.getOnrampQuote`
- `payments.getPaymentReceipt`
- `payments.getPremiumGiftCodeOptions`
- `payments.getSavedInfo`
- `payments.getSavedStarGift`
- `payments.getStarGiftActiveAuctions`
- `payments.getStarGiftAuctionAcquiredGifts`
- `payments.getStarGiftWithdrawalUrl`
- `payments.getStarsGiftOptions`
- `payments.getStarsGiveawayOptions`
- `payments.getStarsRevenueAdsAccountUrl`
- `payments.getStarsRevenueStats`
- `payments.getStarsRevenueWithdrawalUrl`
- `payments.getStarsSubscriptions`
- `payments.getStarsTopupOptions`
- `payments.getStarsTransactionsByID`
- `payments.getSuggestedStarRefBots`
- `payments.launchPrepaidGiveaway`
- `payments.toggleChatStarGiftNotifications`
- `payments.validateRequestedInfo`
- `payments.withdrawStarGift`

</details>

<details><summary>phone (42)</summary>

- `phone.acceptCall`
- `phone.checkGroupCall`
- `phone.confirmCall`
- `phone.createConferenceCall`
- `phone.createGroupCall`
- `phone.declineConferenceCallInvite`
- `phone.deleteConferenceCallParticipants`
- `phone.deleteGroupCallMessages`
- `phone.deleteGroupCallParticipantMessages`
- `phone.discardCall`
- `phone.discardGroupCall`
- `phone.editGroupCallParticipant`
- `phone.editGroupCallTitle`
- `phone.exportGroupCallInvite`
- `phone.getCallConfig`
- `phone.getGroupCall`
- `phone.getGroupCallChainBlocks`
- `phone.getGroupCallJoinAs`
- `phone.getGroupCallStars`
- `phone.getGroupCallStreamChannels`
- `phone.getGroupCallStreamRtmpUrl`
- `phone.inviteConferenceCallParticipant`
- `phone.inviteToGroupCall`
- `phone.joinGroupCall`
- `phone.joinGroupCallPresentation`
- `phone.leaveGroupCall`
- `phone.leaveGroupCallPresentation`
- `phone.receivedCall`
- `phone.requestCall`
- `phone.saveCallDebug`
- `phone.saveCallLog`
- `phone.saveDefaultGroupCallJoinAs`
- `phone.saveDefaultSendAs`
- `phone.sendConferenceCallBroadcast`
- `phone.sendGroupCallEncryptedMessage`
- `phone.sendGroupCallMessage`
- `phone.sendSignalingData`
- `phone.setCallRating`
- `phone.startScheduledGroupCall`
- `phone.toggleGroupCallRecord`
- `phone.toggleGroupCallSettings`
- `phone.toggleGroupCallStartSubscription`

</details>

<details><summary>photos (1)</summary>

- `photos.uploadContactProfilePhoto`

</details>

<details><summary>premium (2)</summary>

- `premium.getBoostsList`
- `premium.getUserBoosts`

</details>

<details><summary>stats (8)</summary>

- `stats.getBroadcastStats`
- `stats.getMegagroupStats`
- `stats.getMessagePublicForwards`
- `stats.getMessageStats`
- `stats.getPollStats`
- `stats.getStoryPublicForwards`
- `stats.getStoryStats`
- `stats.loadAsyncGraph`

</details>

<details><summary>stickers (1)</summary>

- `stickers.checkShortName`

</details>

<details><summary>stories (17)</summary>

- `stories.createAlbum`
- `stories.deleteAlbum`
- `stories.exportStoryLink`
- `stories.getAlbumStories`
- `stories.getAlbums`
- `stories.getAllReadPeerStories`
- `stories.getChatsToSend`
- `stories.getPeerMaxIDs`
- `stories.getStoriesViews`
- `stories.getStoryReactionsList`
- `stories.reorderAlbums`
- `stories.report`
- `stories.searchPosts`
- `stories.startLive`
- `stories.toggleAllStoriesHidden`
- `stories.togglePinnedToTop`
- `stories.updateAlbum`

</details>

<details><summary>toncenter (2)</summary>

- `toncenter.getStreamingUrl`
- `toncenter.performApiRequest`

</details>

<details><summary>upload (1)</summary>

- `upload.getWebFile`

</details>

<details><summary>users (3)</summary>

- `users.getRequirementsToContact`
- `users.getSavedMusicByID`
- `users.setSecureValueErrors`

</details>

<details><summary>wallet (23)</summary>

- `wallet.disableBackup`
- `wallet.enableBackup`
- `wallet.exportSecretPhrase`
- `wallet.fetchEncryptedSecretPhrasePart`
- `wallet.getBackupHolderDcs`
- `wallet.getExistingWaltBalance`
- `wallet.getGaslessInfo`
- `wallet.getNfts`
- `wallet.getState`
- `wallet.getTransactions`
- `wallet.getTransactionsByIDs`
- `wallet.getTransactionsByMsgHash`
- `wallet.sendTransfer`
- `wallet.setCardStickers`
- `wallet.tonConnectClaimRequest`
- `wallet.tonConnectCloseSession`
- `wallet.tonConnectCreateSession`
- `wallet.tonConnectGetPending`
- `wallet.tonConnectGetSessions`
- `wallet.tonConnectNextEventId`
- `wallet.tonConnectRegisterKey`
- `wallet.tonConnectSubmitConnectResult`
- `wallet.tonConnectSubmitResponse`

</details>


## Bot API parity

Bot API 10.3: 185 methods, 400 types. 34 methods and 107 types have no counterpart here.

<details><summary>Methods (34)</summary>

- `banChatSenderChat`
- `copyMessages`
- `createChatSubscriptionInviteLink`
- `deleteChatStickerSet`
- `deleteStory`
- `editChatSubscriptionInviteLink`
- `editMessageLiveLocation`
- `editStory`
- `getForumTopicIconStickers`
- `getStarTransactions`
- `getUserChatBoosts`
- `getUserProfileAudios`
- `postStory`
- `readBusinessMessage`
- `removeBusinessAccountProfilePhoto`
- `removeChatVerification`
- `removeMyProfilePhoto`
- `removeUserVerification`
- `repostStory`
- `savePreparedInlineMessage`
- `savePreparedKeyboardButton`
- `setBusinessAccountBio`
- `setBusinessAccountGiftSettings`
- `setBusinessAccountName`
- `setBusinessAccountProfilePhoto`
- `setBusinessAccountUsername`
- `setChatStickerSet`
- `setMyProfilePhoto`
- `setPassportDataErrors`
- `setUserEmojiStatus`
- `stopMessageLiveLocation`
- `unbanChatSenderChat`
- `verifyChat`
- `verifyUser`

</details>

<details><summary>Types (107)</summary>

- `AffiliateInfo`
- `BackgroundFill`
- `BackgroundFillFreeformGradient`
- `BackgroundFillGradient`
- `BackgroundFillSolid`
- `BackgroundType`
- `BackgroundTypeChatTheme`
- `BackgroundTypeFill`
- `BackgroundTypePattern`
- `BackgroundTypeWallpaper`
- `BotDescription`
- `BotName`
- `BotShortDescription`
- `BotSubscriptionUpdated`
- `BusinessLocation`
- `BusinessMessagesDeleted`
- `ChatBoostAdded`
- `ChatBoostRemoved`
- `ChatBoostSource`
- `ChatBoostSourceGiftCode`
- `ChatBoostSourceGiveaway`
- `ChatBoostSourcePremium`
- `ChatLocation`
- `EncryptedCredentials`
- `EncryptedPassportElement`
- `GiftBackground`
- `GiftInfo`
- `Gifts`
- `InaccessibleMessage`
- `InlineQueryResultCachedMpeg4Gif`
- `InlineQueryResultGame`
- `InlineQueryResultMpeg4Gif`
- `InlineQueryResultsButton`
- `InputPaidMedia`
- `InputPaidMediaLivePhoto`
- `InputPaidMediaPhoto`
- `InputPaidMediaVideo`
- `InputProfilePhoto`
- `InputProfilePhotoAnimated`
- `InputProfilePhotoStatic`
- `InputStoryContent`
- `InputStoryContentPhoto`
- `InputStoryContentVideo`
- `LocationAddress`
- `MaybeInaccessibleMessage`
- `MessageAutoDeleteTimerChanged`
- `OwnedGift`
- `OwnedGiftRegular`
- `OwnedGiftUnique`
- `OwnedGifts`
- `PaidMedia`
- `PaidMediaLivePhoto`
- `PaidMediaPhoto`
- `PaidMediaPurchased`
- `PaidMediaVideo`
- `PaidMessagePriceChanged`
- `PassportData`
- `PassportElementError`
- `PassportElementErrorDataField`
- `PassportElementErrorFile`
- `PassportElementErrorFiles`
- `PassportElementErrorFrontSide`
- `PassportElementErrorReverseSide`
- `PassportElementErrorSelfie`
- `PassportElementErrorTranslationFile`
- `PassportElementErrorTranslationFiles`
- `PassportElementErrorUnspecified`
- `PassportFile`
- `PollAnswer`
- `PollMedia`
- `PreparedInlineMessage`
- `PreparedKeyboardButton`
- `RevenueWithdrawalState`
- `RevenueWithdrawalStateFailed`
- `RevenueWithdrawalStatePending`
- `RevenueWithdrawalStateSucceeded`
- `SharedUser`
- `StarTransaction`
- `StarTransactions`
- `StoryArea`
- `StoryAreaPosition`
- `StoryAreaType`
- `StoryAreaTypeLink`
- `StoryAreaTypeLocation`
- `StoryAreaTypeSuggestedReaction`
- `StoryAreaTypeUniqueGift`
- `StoryAreaTypeWeather`
- `TransactionPartner`
- `TransactionPartnerAffiliateProgram`
- `TransactionPartnerChat`
- `TransactionPartnerFragment`
- `TransactionPartnerOther`
- `TransactionPartnerTelegramAds`
- `TransactionPartnerTelegramApi`
- `TransactionPartnerUser`
- `UniqueGift`
- `UniqueGiftBackdrop`
- `UniqueGiftBackdropColors`
- `UniqueGiftColors`
- `UniqueGiftInfo`
- `UniqueGiftModel`
- `UniqueGiftSymbol`
- `UserChatBoosts`
- `UserProfileAudios`
- `UserProfilePhotos`
- `VideoChatParticipantsInvited`
- `VideoQuality`

</details>
