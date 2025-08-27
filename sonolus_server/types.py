from typing import Literal

type localization = str # Literal['el', 'en', 'es', 'fr', 'id', 'it', 'ja', 'ko', 'ru', 'tr', 'zhs', 'zht']
type ServerInfoButton_type = Literal['authentication', 'multiplayer', 'post', 'playlist', 'level', 'replay', 'skin', 'background', 'effect', 'particle', 'engine', 'configuration']
type number = int | float
type ItemType = Literal['post', 'playlist', 'level', 'skin', 'background', 'effect', 'particle', 'engine', 'replay', 'room']

type Text = Literal[ # https://github.com/Sonolus/sonolus-core/blob/main/src/common/core/text.ts
    '#CUSTOM_SERVER', # en: Custom Server
    '#COLLECTION', # en: Collection
    '#SERVER', # en: Server
    '#ADDRESS', # en: Address
    '#EXPIRATION', # en: Expiration
    '#STORAGE', # en: Storage
    '#LOG', # en: Log
    '#INQUIRY', # en: Inquiry
    '#BANNER', # en: Banner
    '#POST', # en: Post
    '#PLAYLIST', # en: Playlist
    '#LEVEL', # en: Level
    '#SKIN', # en: Skin
    '#BACKGROUND', # en: Background
    '#EFFECT', # en: SFX
    '#PARTICLE', # en: Particle
    '#ENGINE', # en: Engine
    '#REPLAY', # en: Replay
    '#ROOM', # en: Room
    '#POST_THUMBNAIL', # en: Thumbnail
    '#PLAYLIST_THUMBNAIL', # en: Thumbnail
    '#LEVEL_COVER', # en: Cover
    '#LEVEL_BGM', # en: BGM
    '#LEVEL_PREVIEW', # en: Preview
    '#LEVEL_DATA', # en: Data
    '#SKIN_THUMBNAIL', # en: Thumbnail
    '#SKIN_DATA', # en: Data
    '#SKIN_TEXTURE', # en: Texture
    '#BACKGROUND_THUMBNAIL', # en: Thumbnail
    '#BACKGROUND_IMAGE', # en: Image
    '#BACKGROUND_DATA', # en: Data
    '#BACKGROUND_CONFIGURATION', # en: Configuration
    '#EFFECT_THUMBNAIL', # en: Thumbnail
    '#EFFECT_DATA', # en: Data
    '#EFFECT_AUDIO', # en: Audio
    '#PARTICLE_THUMBNAIL', # en: Thumbnail
    '#PARTICLE_DATA', # en: Data
    '#PARTICLE_TEXTURE', # en: Texture
    '#ENGINE_THUMBNAIL', # en: Thumbnail
    '#ENGINE_PLAYDATA', # en: Play Data
    '#ENGINE_WATCHDATA', # en: Watch Data
    '#ENGINE_PREVIEWDATA', # en: Preview Data
    '#ENGINE_TUTORIALDATA', # en: Tutorial Data
    '#ENGINE_ROM', # en: ROM
    '#ENGINE_CONFIGURATION', # en: Configuration
    '#REPLAY_DATA', # en: Data
    '#REPLAY_CONFIGURATION', # en: Configuration
    '#ROOM_COVER', # en: Cover
    '#ROOM_BGM', # en: BGM
    '#ROOM_PREVIEW', # en: Preview
    '#GRADE', # en: Grade
    '#ARCADE_SCORE', # en: Arcade Score
    '#ACCURACY_SCORE', # en: Accuracy Score
    '#COMBO', # en: Combo
    '#PERFECT', # en: Perfect
    '#GREAT', # en: Great
    '#GOOD', # en: Good
    '#MISS', # en: Miss
    '#FILTER', # en: Filter
    '#SORT', # en: Sort
    '#KEYWORDS', # en: Keywords
    '#NAME', # en: Name
    '#RATING', # en: Rating
    '#RATING_MINIMUM', # en: Minimum Rating
    '#RATING_MAXIMUM', # en: Maximum Rating
    '#TITLE', # en: Title
    '#SUBTITLE', # en: Subtitle
    '#ARTISTS', # en: Artists
    '#TIME', # en: Time
    '#AUTHOR', # en: Author
    '#DESCRIPTION', # en: Description
    '#GENRE', # en: Genre
    '#TYPE', # en: Type
    '#CATEGORY', # en: Category
    '#STATUS', # en: Status
    '#LANGUAGE', # en: Language
    '#DIFFICULTY', # en: Difficulty
    '#VERSION', # en: Version
    '#LENGTH', # en: Length
    '#LENGTH_MINIMUM', # en: Minimum Length
    '#LENGTH_MAXIMUM', # en: Maximum Length
    '#ADDITIONAL_INFORMATION', # en: Additional Information
    '#TIMEZONE', # en: Timezone
    '#REGION', # en: Region
    '#CONTENT', # en: Content
    '#COMMENT', # en: Comment
    '#MESSAGE', # en: Message
    '#ROLE', # en: Role
    '#PERMISSION', # en: Permission
    '#USER', # en: User
    '#SPEED', # en: Level Speed
    '#MIRROR', # en: Mirror Level
    '#RANDOM', # en: Random
    '#HIDDEN', # en: Hidden
    '#JUDGMENT_STRICT', # en: Strict Judgment
    '#JUDGMENT_LOOSE', # en: Loose Judgment
    '#EFFECT_AUTO', # en: Auto SFX
    '#STAGE', # en: Stage
    '#STAGE_POSITION', # en: Stage Position
    '#STAGE_SIZE', # en: Stage Size
    '#STAGE_ROTATION', # en: Stage Rotation
    '#STAGE_DIRECTION', # en: Stage Direction
    '#STAGE_ALPHA', # en: Stage Transparency
    '#STAGE_ANIMATION', # en: Stage Animation
    '#STAGE_TILT', # en: Stage Tilt
    '#STAGE_COVER_VERTICAL', # en: Vertical Stage Cover
    '#STAGE_COVER_HORIZONTAL', # en: Horizontal Stage Cover
    '#STAGE_COVER_ALPHA', # en: Stage Cover Transparency
    '#STAGE_ASPECTRATIO_LOCK', # en: Lock Stage Aspect Ratio
    '#STAGE_EFFECT', # en: Stage Effect
    '#STAGE_EFFECT_POSITION', # en: Stage Effect Position
    '#STAGE_EFFECT_SIZE', # en: Stage Effect Size
    '#STAGE_EFFECT_ROTATION', # en: Stage Effect Rotation
    '#STAGE_EFFECT_DIRECTION', # en: Stage Effect Direction
    '#STAGE_EFFECT_ALPHA', # en: Stage Effect Transparency
    '#LANE', # en: Lane
    '#LANE_POSITION', # en: Lane Position
    '#LANE_SIZE', # en: Lane Size
    '#LANE_ROTATION', # en: Lane Rotation
    '#LANE_DIRECTION', # en: Lane Direction
    '#LANE_ALPHA', # en: Lane Transparency
    '#LANE_ANIMATION', # en: Lane Animation
    '#LANE_EFFECT', # en: Lane Effect
    '#LANE_EFFECT_POSITION', # en: Lane Effect Position
    '#LANE_EFFECT_SIZE', # en: Lane Effect Size
    '#LANE_EFFECT_ROTATION', # en: Lane Effect Rotation
    '#LANE_EFFECT_DIRECTION', # en: Lane Effect Direction
    '#LANE_EFFECT_ALPHA', # en: Lane Effect Transparency
    '#JUDGELINE', # en: Judgment Line
    '#JUDGELINE_POSITION', # en: Judgment Line Position
    '#JUDGELINE_SIZE', # en: Judgment Line Size
    '#JUDGELINE_ROTATION', # en: Judgment Line Rotation
    '#JUDGELINE_DIRECTION', # en: Judgment Line Direction
    '#JUDGELINE_ALPHA', # en: Judgment Line Transparency
    '#JUDGELINE_ANIMATION', # en: Judgment Line Animation
    '#JUDGELINE_EFFECT', # en: Judgment Line Effect
    '#JUDGELINE_EFFECT_POSITION', # en: Judgment Line Effect Position
    '#JUDGELINE_EFFECT_SIZE', # en: Judgment Line Effect Size
    '#JUDGELINE_EFFECT_ROTATION', # en: Judgment Line Effect Rotation
    '#JUDGELINE_EFFECT_DIRECTION', # en: Judgment Line Effect Direction
    '#JUDGELINE_EFFECT_ALPHA', # en: Judgment Line Effect Transparency
    '#SLOT', # en: Slot
    '#SLOT_POSITION', # en: Slot Position
    '#SLOT_SIZE', # en: Slot Size
    '#SLOT_ROTATION', # en: Slot Rotation
    '#SLOT_DIRECTION', # en: Slot Direction
    '#SLOT_ALPHA', # en: Slot Transparency
    '#SLOT_ANIMATION', # en: Slot Animation
    '#SLOT_EFFECT', # en: Slot Effect
    '#SLOT_EFFECT_POSITION', # en: Slot Effect Position
    '#SLOT_EFFECT_SIZE', # en: Slot Effect Size
    '#SLOT_EFFECT_ROTATION', # en: Slot Effect Rotation
    '#SLOT_EFFECT_DIRECTION', # en: Slot Effect Direction
    '#SLOT_EFFECT_ALPHA', # en: Slot Effect Transparency
    '#NOTE', # en: Note
    '#NOTE_SPEED', # en: Note Speed
    '#NOTE_SPEED_RANDOM', # en: Random Note Speed
    '#NOTE_POSITION', # en: Note Position
    '#NOTE_SIZE', # en: Note Size
    '#NOTE_ROTATION', # en: Note Rotation
    '#NOTE_DIRECTION', # en: Note Direction
    '#NOTE_COLOR', # en: Note Color
    '#NOTE_ALPHA', # en: Note Transparency
    '#NOTE_ANIMATION', # en: Note Animation
    '#NOTE_EFFECT', # en: Note Effect
    '#NOTE_EFFECT_POSITION', # en: Note Effect Position
    '#NOTE_EFFECT_SIZE', # en: Note Effect Size
    '#NOTE_EFFECT_ROTATION', # en: Note Effect Rotation
    '#NOTE_EFFECT_DIRECTION', # en: Note Effect Direction
    '#NOTE_EFFECT_COLOR', # en: Note Effect Color
    '#NOTE_EFFECT_ALPHA', # en: Note Effect Transparency
    '#MARKER', # en: Marker
    '#MARKER_POSITION', # en: Marker Position
    '#MARKER_SIZE', # en: Marker Size
    '#MARKER_ROTATION', # en: Marker Rotation
    '#MARKER_DIRECTION', # en: Marker Direction
    '#MARKER_COLOR', # en: Marker Color
    '#MARKER_ALPHA', # en: Marker Transparency
    '#MARKER_ANIMATION', # en: Marker Animation
    '#CONNECTOR', # en: Connector
    '#CONNECTOR_POSITION', # en: Connector Position
    '#CONNECTOR_SIZE', # en: Connector Size
    '#CONNECTOR_ROTATION', # en: Connector Rotation
    '#CONNECTOR_DIRECTION', # en: Connector Direction
    '#CONNECTOR_COLOR', # en: Connector Color
    '#CONNECTOR_ALPHA', # en: Connector Transparency
    '#CONNECTOR_ANIMATION', # en: Connector Animation
    '#SIMLINE', # en: Simultaneous Line
    '#SIMLINE_POSITION', # en: Simultaneous Line Position
    '#SIMLINE_SIZE', # en: Simultaneous Line Size
    '#SIMLINE_ROTATION', # en: Simultaneous Line Rotation
    '#SIMLINE_DIRECTION', # en: Simultaneous Line Direction
    '#SIMLINE_COLOR', # en: Simultaneous Line Color
    '#SIMLINE_ALPHA', # en: Simultaneous Line Transparency
    '#SIMLINE_ANIMATION', # en: Simultaneous Line Animation
    '#PREVIEW_SCALE_VERTICAL', # en: Preview Vertical Scale
    '#PREVIEW_SCALE_HORIZONTAL', # en: Preview Horizontal Scale
    '#PREVIEW_TIME', # en: Preview Time
    '#PREVIEW_SCORE', # en: Preview Score
    '#PREVIEW_BPM', # en: Preview BPM
    '#PREVIEW_TIMESCALE', # en: Preview Time Scale
    '#PREVIEW_BEAT', # en: Preview Beat
    '#PREVIEW_MEASURE', # en: Preview Measure
    '#PREVIEW_COMBO', # en: Preview Combo
    '#NONE', # en: None
    '#ANY', # en: Any
    '#ALL', # en: All
    '#OTHERS', # en: Others
    '#SHORT', # en: Short
    '#LONG', # en: Long
    '#HIGH', # en: High
    '#MID', # en: Mid
    '#LOW', # en: Low
    '#SMALL', # en: Small
    '#MEDIUM', # en: Medium
    '#LARGE', # en: Large
    '#LEFT', # en: Left
    '#RIGHT', # en: Right
    '#UP', # en: Up
    '#DOWN', # en: Down
    '#FRONT', # en: Front
    '#BACK', # en: Back
    '#CENTER', # en: Center
    '#TOP', # en: Top
    '#BOTTOM', # en: Bottom
    '#TOP_LEFT', # en: Top Left
    '#TOP_CENTER', # en: Top Center
    '#TOP_RIGHT', # en: Top Right
    '#CENTER_LEFT', # en: Center Left
    '#CENTER_RIGHT', # en: Center Right
    '#BOTTOM_LEFT', # en: Bottom Left
    '#BOTTOM_CENTER', # en: Bottom Center
    '#BOTTOM_RIGHT', # en: Bottom Right
    '#CLOCKWISE', # en: Clockwise
    '#COUNTERCLOCKWISE', # en: Counterclockwise
    '#FORWARD', # en: Forward
    '#BACKWARD', # en: Backward
    '#DEFAULT', # en: Default
    '#NEUTRAL', # en: Neutral
    '#RED', # en: Red
    '#GREEN', # en: Green
    '#BLUE', # en: Blue
    '#YELLOW', # en: Yellow
    '#PURPLE', # en: Purple
    '#CYAN', # en: Cyan
    '#SIMPLE', # en: Simple
    '#EASY', # en: Easy
    '#NORMAL', # en: Normal
    '#HARD', # en: Hard
    '#EXPERT', # en: Expert
    '#MASTER', # en: Master
    '#PRO', # en: Pro
    '#TECHNICAL', # en: Technical
    '#SPECIAL', # en: Special
    '#KEYWORDS_PLACEHOLDER', # en: Enter keywords...
    '#NAME_PLACEHOLDER', # en: Enter name...
    '#RATING_PLACEHOLDER', # en: Enter rating...
    '#RATING_MINIMUM_PLACEHOLDER', # en: Enter minimum rating...
    '#RATING_MAXIMUM_PLACEHOLDER', # en: Enter maximum rating...
    '#TITLE_PLACEHOLDER', # en: Enter title...
    '#SUBTITLE_PLACEHOLDER', # en: Enter subtitle...
    '#ARTISTS_PLACEHOLDER', # en: Enter artists...
    '#TIME_PLACEHOLDER', # en: Enter time...
    '#AUTHOR_PLACEHOLDER', # en: Enter author...
    '#DESCRIPTION_PLACEHOLDER', # en: Enter description...
    '#GENRE_PLACEHOLDER', # en: Enter genre...
    '#TYPE_PLACEHOLDER', # en: Enter type...
    '#CATEGORY_PLACEHOLDER', # en: Enter category...
    '#LANGUAGE_PLACEHOLDER', # en: Enter language...
    '#DIFFICULTY_PLACEHOLDER', # en: Enter difficulty...
    '#LENGTH_PLACEHOLDER', # en: Enter length...
    '#LENGTH_MINIMUM_PLACEHOLDER', # en: Enter minimum length...
    '#LENGTH_MAXIMUM_PLACEHOLDER', # en: Enter maximum length...
    '#ADDITIONAL_INFORMATION_PLACEHOLDER', # en: Enter additional information...
    '#TIMEZONE_PLACEHOLDER', # en: Enter timezone...
    '#REGION_PLACEHOLDER', # en: Enter region...
    '#CONTENT_PLACEHOLDER', # en: Enter content...
    '#COMMENT_PLACEHOLDER', # en: Enter comment...
    '#REVIEW_PLACEHOLDER', # en: Enter review...
    '#REPLY_PLACEHOLDER', # en: Enter reply...
    '#MESSAGE_PLACEHOLDER', # en: Enter message...
    '#ROLE_PLACEHOLDER', # en: Enter role...
    '#PERMISSION_PLACEHOLDER', # en: Enter permission...
    '#USER_PLACEHOLDER', # en: Enter user...
    '#PERCENTAGE_UNIT', # en: {0}%
    '#YEAR_UNIT', # en: {0} yr
    '#MONTH_UNIT', # en: {0} mo
    '#DAY_UNIT', # en: {0} d
    '#HOUR_UNIT', # en: {0} h
    '#MINUTE_UNIT', # en: {0} m
    '#SECOND_UNIT', # en: {0} s
    '#MILLISECOND_UNIT', # en: {0} ms
    '#YEAR_PAST', # en: {0} yr ago
    '#MONTH_PAST', # en: {0} mo ago
    '#DAY_PAST', # en: {0} d ago
    '#HOUR_PAST', # en: {0} h ago
    '#MINUTE_PAST', # en: {0} m ago
    '#SECOND_PAST', # en: {0} s ago
    '#MILLISECOND_PAST', # en: {0} ms ago
    '#YEAR_FUTURE', # en: In {0} yr
    '#MONTH_FUTURE', # en: In {0} mo
    '#DAY_FUTURE', # en: In {0} d
    '#HOUR_FUTURE', # en: In {0} h
    '#MINUTE_FUTURE', # en: In {0} m
    '#SECOND_FUTURE', # en: In {0} s
    '#MILLISECOND_FUTURE', # en: In {0} ms
    '#TAP', # en: Tap
    '#TAP_HOLD', # en: Tap and Hold
    '#TAP_RELEASE', # en: Tap and Release
    '#TAP_FLICK', # en: Tap and Flick
    '#TAP_SLIDE', # en: Tap and Slide
    '#HOLD', # en: Hold
    '#HOLD_SLIDE', # en: Hold and Slide
    '#HOLD_FOLLOW', # en: Hold and Follow
    '#RELEASE', # en: Release
    '#FLICK', # en: Flick
    '#SLIDE', # en: Slide
    '#SLIDE_FLICK', # en: Slide and Flick
    '#AVOID', # en: Avoid
    '#JIGGLE', # en: Jiggle
    '#NEWEST', # en: Newest
    '#OLDEST', # en: Oldest
    '#RECOMMENDED', # en: Recommended
    '#POPULAR', # en: Popular
    '#FEATURED', # en: Featured
    '#COMPETITIVE', # en: Competitive
    '#HOLIDAY', # en: Holiday
    '#LIMITED', # en: Limited
    '#ANNOUNCEMENT', # en: Announcement
    '#INFORMATION', # en: Information
    '#HELP', # en: Help
    '#MAINTENANCE', # en: Maintenance
    '#EVENT', # en: Event
    '#UPDATE', # en: Update
    '#SEARCH', # en: Search
    '#ADVANCED', # en: Advanced
    '#RELATED', # en: Related
    '#SAME_AUTHOR', # en: Same Author
    '#SAME_ARTISTS', # en: Same Artists
    '#SAME_RATING', # en: Same Rating
    '#SAME_CATEGORY', # en: Same Category
    '#SAME_DIFFICULTY', # en: Same Difficulty
    '#SAME_GENRE', # en: Same Genre
    '#SAME_VERSION', # en: Same Version
    '#OTHER_AUTHORS', # en: Other Authors
    '#OTHER_ARTISTS', # en: Other Artists
    '#OTHER_RATINGS', # en: Other Ratings
    '#OTHER_CATEGORIES', # en: Other Categories
    '#OTHER_DIFFICULTIES', # en: Other Difficulties
    '#OTHER_GENRES', # en: Other Genres
    '#OTHER_VERSIONS', # en: Other Versions
    '#DRAFT', # en: Draft
    '#PUBLIC', # en: Public
    '#PRIVATE', # en: Private
    '#POP', # en: Pop
    '#ROCK', # en: Rock
    '#HIPHOP', # en: Hip Hop
    '#COUNTRY', # en: Country
    '#ELECTRONIC', # en: Electronic
    '#METAL', # en: Metal
    '#CLASSICAL', # en: Classical
    '#FOLK', # en: Folk
    '#INDIE', # en: Indie
    '#ANIME', # en: Anime
    '#VOCALOID', # en: Vocaloid
    '#REMIX', # en: Remix
    '#INSTRUMENTAL', # en: Instrumental
    '#SHORT_VERSION', # en: Short Version
    '#LONG_VERSION', # en: Long Version
    '#LIVE_VERSION', # en: Live Version
    '#REPORT', # en: Report
    '#REASON', # en: Reason
    '#ILLEGAL_ACTIVITIES', # en: Illegal Activities
    '#CHEATING', # en: Cheating
    '#AFK', # en: AFK
    '#SPAMMING', # en: Spamming
    '#VERBAL_ABUSE', # en: Verbal Abuse
    '#INAPPROPRIATE_LANGUAGE', # en: Inappropriate Language
    '#NEGATIVE_ATTITUDE', # en: Negative Attitude
    '#DNF', # en: DNF
    '#SUGGESTIONS', # en: Suggestions
    '#SUGGESTIONS_PER_PLAYER', # en: Suggestions per Player
    '#MATCH_SCORING', # en: Match Scoring
    '#MATCH_TIEBREAKER', # en: Match Tiebreaker
    '#MATCH_COUNT', # en: Match Count
    '#MATCH_LIMIT', # en: Match Limit
    '#ROUND_SCORING', # en: Round Scoring
    '#ROUND_TIEBREAKER', # en: Round Tiebreaker
    '#ROUND_COUNT', # en: Round Count
    '#ROUND_LIMIT', # en: Round Limit
    '#TEAM_SCORING', # en: Team Scoring
    '#TEAM_TIEBREAKER', # en: Team Tiebreaker
    '#TEAM_COUNT', # en: Team Count
    '#TEAM_LIMIT', # en: Team Limit
    '#QUALIFIED', # en: Qualified
    '#DISQUALIFIED', # en: Disqualified
    '#RANKING', # en: Ranking
    '#SCORE', # en: Score
    '#OWNER', # en: Owner
    '#ADMIN', # en: Admin
    '#MODERATOR', # en: Moderator
    '#REVIEWER', # en: Reviewer
    '#BANNED', # en: Banned
    '#PLAYER', # en: Player
    '#SPECTATOR', # en: Spectator
    '#REFEREE', # en: Referee
    '#ELIMINATED', # en: Eliminated
    '#FINALIST', # en: Finalist
    '#FINISHED', # en: Finished
    '#WINNER', # en: Winner
    '#GOLD_MEDAL', # en: Gold Medal
    '#SILVER_MEDAL', # en: Silver Medal
    '#BRONZE_MEDAL', # en: Bronze Medal
    '#TEAM_1', # en: Team 1
    '#TEAM_2', # en: Team 2
    '#TEAM_3', # en: Team 3
    '#TEAM_4', # en: Team 4
    '#TEAM_5', # en: Team 5
    '#TEAM_6', # en: Team 6
    '#TEAM_7', # en: Team 7
    '#TEAM_8', # en: Team 8
    '#TEAM_RED', # en: Team Red
    '#TEAM_GREEN', # en: Team Green
    '#TEAM_BLUE', # en: Team Blue
    '#TEAM_YELLOW', # en: Team Yellow
    '#TEAM_PURPLE', # en: Team Purple
    '#TEAM_CYAN', # en: Team Cyan
    '#TEAM_WHITE', # en: Team White
    '#TEAM_BLACK', # en: Team Black
    '#REPLY', # en: Reply
    '#REPLIED', # en: Replied
    '#REVIEW', # en: Review
    '#REVIEWING', # en: Reviewing
    '#REVIEWED', # en: Reviewed
    '#VERIFY', # en: Verify
    '#VERIFYING', # en: Verifying
    '#VERIFIED', # en: Verified
    '#UPLOAD', # en: Upload
    '#UPLOADING', # en: Uploading
    '#UPLOADED', # en: Uploaded
    '#SUBMIT', # en: Submit
    '#SUBMITTING', # en: Submitting
    '#SUBMITTED', # en: Submitted
    '#EDIT', # en: Edit
    '#EDITING', # en: Editing
    '#EDITED', # en: Edited
    '#LIKE', # en: Like
    '#LIKED', # en: Liked
    '#DISLIKE', # en: Dislike
    '#DISLIKED', # en: Disliked
    '#BOOKMARK', # en: Bookmark
    '#BOOKMARKED', # en: Bookmarked
    '#DELETE', # en: Delete
    '#DELETING', # en: Deleting
    '#DELETED', # en: Deleted
    '#REMOVE', # en: Remove
    '#REMOVING', # en: Removing
    '#REMOVED', # en: Removed
    '#RESTORE', # en: Restore
    '#RESTORING', # en: Restoring
    '#RESTORED', # en: Restored
    '#CONFIRM', # en: Confirm
    '#CONFIRMED', # en: Confirmed
    '#CANCEL', # en: Cancel
    '#CANCELED', # en: Canceled
    '#INCREASE', # en: Increase
    '#DECREASE', # en: Decrease
    '#UPVOTE', # en: Upvote
    '#UPVOTED', # en: Upvoted
    '#DOWNVOTE', # en: Downvote
    '#DOWNVOTED', # en: Downvoted
    '#AGREE', # en: Agree
    '#AGREED', # en: Agreed
    '#DISAGREE', # en: Disagree
    '#DISAGREED', # en: Disagreed
    '#LOCK', # en: Lock
    '#LOCKED', # en: Locked
    '#UNLOCK', # en: Unlock
    '#UNLOCKED', # en: Unlocked
    '#PIN', # en: Pin
    '#PINNED', # en: Pinned
    '#UNPIN', # en: Unpin
    '#UNPINNED', # en: Unpinned
    '#FOLLOW', # en: Follow
    '#FOLLOWING', # en: Following
    '#FOLLOWED', # en: Followed
    '#UNFOLLOW', # en: Unfollow
    '#SUBSCRIBE', # en: Subscribe
    '#SUBSCRIBING', # en: Subscribing
    '#SUBSCRIBED', # en: Subscribed
    '#UNSUBSCRIBE', # en: Unsubscribe
    '#PUBLISH', # en: Publish
    '#PUBLISHING', # en: Publishing
    '#PUBLISHED', # en: Published
    '#UNPUBLISH', # en: Unpublish
    '#SHOW', # en: Show
    '#HIDE', # en: Hide
    '#ALLOW', # en: Allow
    '#ALLOWED', # en: Allowed
    '#DISALLOW', # en: Disallow
    '#DISALLOWED', # en: Disallowed
    '#APPROVE', # en: Approve
    '#APPROVED', # en: Approved
    '#DENY', # en: Deny
    '#DENIED', # en: Denied
    '#ACCEPT', # en: Accept
    '#ACCEPTED', # en: Accepted
    '#REJECT', # en: Reject
    '#REJECTED', # en: Rejected
    '#STAR', # en: Star
    '#STARRED', # en: Starred
]

type Icon = Literal[ # https://github.com/Sonolus/sonolus-core/blob/main/src/common/core/icon.ts
    'advanced',
    'angleDown',
    'angleLeft',
    'angleRight',
    'anglesDown',
    'anglesLeft',
    'anglesRight',
    'anglesUp',
    'angleUp',
    'arrowDown',
    'arrowLeft',
    'arrowRight',
    'arrowUp',
    'award',
    'background',
    'bell',
    'bellSlash',
    'bookmark',
    'bookmarkHollow',
    'check',
    'clock',
    'comment',
    'crown',
    'customServer',
    'delete',
    'edit',
    'effect',
    'engine',
    'envelope',
    'envelopeOpen',
    'globe',
    'heart',
    'heartHollow',
    'hide',
    'information',
    'level',
    'lock',
    'medal',
    'message',
    'minus',
    'options',
    'particle',
    'pin',
    'player',
    'playlist',
    'plus',
    'post',
    'question',
    'ranking',
    'replay',
    'reply',
    'restore',
    'room',
    'search',
    'settings',
    'show',
    'shuffle',
    'skin',
    'star',
    'starHalf',
    'starHollow',
    'stopwatch',
    'tag',
    'thumbsDown',
    'thumbsDownHollow',
    'thumbsUp',
    'thumbsUpHollow',
    'trophy',
    'unlock',
    'xMark',
]